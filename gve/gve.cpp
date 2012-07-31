#include <iostream>
#include <vector>
#include <cassert>
#include <time.h>
#include <sys/time.h>


/*
 *
 * terminal bit ::= 0
 * continuation bit ::= 1
 *
 */

#define MASK7_CONT   (1 << 7)

#define MASK7_DATA_0 ((1 << 7) - 1)
#define MASK7_DATA_1 (((1 << 7) - 1) << 7)
#define MASK7_DATA_2 (((1 << 7) - 1) << 14)
#define MASK7_DATA_3 (((1 << 7) - 1) << 21)

#define MASK8_DATA_0 ((1 << 8) - 1)
#define MASK8_DATA_1 (((1 << 8) - 1) << 8)
#define MASK8_DATA_2 (((1 << 8) - 1) << 16)
#define MASK8_DATA_3 (((1 << 8) - 1) << 24)

#define CLASS7_0_MAX ((1 << 7) - 1)
#define CLASS7_1_MAX ((1 << 14) - 1)
#define CLASS7_2_MAX ((1 << 21) - 1)
#define CLASS7_3_MAX ((1 << 28) - 1)

#define CLASS8_0_MAX ((1 << 8) - 1)
#define CLASS8_1_MAX ((1 << 16) - 1)
#define CLASS8_2_MAX ((1 << 24) - 1)
#define CLASS8_3_MAX ((1 << 32) - 1)

int find_cls7(unsigned int value)
{

    if (value > CLASS7_0_MAX)
    {
        if (value > CLASS7_1_MAX)
        {
            if (value > CLASS7_2_MAX)
            {
                if (value > CLASS7_3_MAX)
                {
                    return -1;
                }
                else
                {
                    return 3;
                }
            }
            else
            {
                return 2;
            }
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
}

int find_cls8(unsigned int value)
{
    if (value > CLASS8_0_MAX)
    {
        if (value > CLASS8_1_MAX)
        {
            if (value > CLASS8_2_MAX)
            {
                return 3;
            }
            else
            {
                return 2;
            }
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 0;
    }
}


void GVE_enc(
        std::vector<unsigned char>& out,
        std::vector<unsigned int> & input
        )
{
    assert (input.size() % 4 == 0);


    std::vector<unsigned int>::iterator itr = input.begin();
    std::vector<unsigned int>::iterator end = input.end();

    int tags[4];
    unsigned int value;
    while (itr != end)
    {
        int tag_index = out.size();
        out.push_back(0);


        for (int i = 0; i < 4; ++i, ++itr)
        {
            value   = *itr;
            tags[i] = find_cls8(value);

            // these routine can be optimized, exploit the little endian env.
            switch(tags[i])
            {
                case 0:
                    out.push_back(value);
                    break;
                case 1:
                    out.push_back(value & MASK8_DATA_0);
                    out.push_back((value & MASK8_DATA_1) >> 8);
                    break;
                case 2:
                    out.push_back(value & MASK8_DATA_0);
                    out.push_back((value & MASK8_DATA_1) >> 8);
                    out.push_back((value & MASK8_DATA_2) >> 16);
                    break;
                case 3:
                    out.push_back(value & MASK8_DATA_0);
                    out.push_back((value & MASK8_DATA_1) >> 8);
                    out.push_back((value & MASK8_DATA_2) >> 16);
                    out.push_back((value & MASK8_DATA_3) >> 24);
                    break;
                default:
                    assert (false);
            }
        }

        /*
         * Tags layout
         *
         * <- MSB
         *      LSB ->
         * ** ** ** **
         * 
         * <- Begin
         *      End ->
         *
         */
        out[tag_index] = (tags[3] & 3) | ((tags[2] & 3) << 2 )| ((tags[1] & 3) << 4 )| ((tags[0] & 3) << 6 );
    }
}

struct DecPlan
{
    int offsets[4];
    unsigned int masks[4];
};

void cls_offset_mask(int cls, int & offset, unsigned int & mask)
{
    switch (cls)
    {
        case 0:
            offset = 1;
            mask   = 0xff;
            break;
        case 1:
            offset = 2;
            mask   = 0xffff;
            break;
        case 2:
            offset = 3;
            mask   = 0xffffff;
            break;
        case 3:
            offset = 4;
            mask   = 0xffffffff;
            break;
    }
}

void gen_dec_plan(std::vector<DecPlan> & dec_plan)
{
    dec_plan.resize(256);
    int id[4];
    for (id[0] = 0; id[0] < 4; ++id[0])
    {
        for (id[1] = 0; id[1] < 4; ++id[1])
        {
            for (id[2] = 0; id[2] < 4; ++id[2])
            {
                for (id[3] = 0; id[3] < 4; ++id[3])
                {
                    int index = (id[0] << 6) + (id[1] << 4) + (id[2] << 2) + id[3];

                    for (int i = 0; i < 4; ++i)
                    {
                        DecPlan dp;
                        cls_offset_mask(id[i], dp.offsets[i], dp.masks[i]);

                        dec_plan[index] = dp;
                    }

                }
            }
        }
    }
}


void GVE_dec(
        const std::vector<DecPlan> & dec_plan,
        std::vector<unsigned int> & out,
        std::vector<unsigned char>& input
        )
{
    std::vector<unsigned char>::iterator itr = input.begin();
    std::vector<unsigned char>::iterator end = input.end();


    for (; itr != end; )
    {
        unsigned char tags = *itr;
        ++itr;
        for (int i = 0; i < 4; ++i)
        {
            int offset = dec_plan[tags].offsets[i];
            unsigned int mask   = dec_plan[tags].masks[i];

            unsigned int * cursor = (unsigned int *)&(*itr);

            out.push_back((*cursor) & mask); // x86 does not have strict boundary condition


            itr += offset;
        }

    }

}


/*
 * LSB part precedes byte order
 *
 */
void BAVE_enc(
        std::vector<unsigned char>& out,
        std::vector<unsigned int> & input
        )
{
    unsigned int value;

    std::vector<unsigned int>::iterator itr = input.begin();
    std::vector<unsigned int>::iterator end = input.end();

    for (; itr != end; ++itr)
    {
        unsigned int value = *itr;
        int cls = find_cls7(value);
        unsigned char enc;
        switch (cls)
        {
            case 0:
                out.push_back((unsigned char )value);
                break;
            case 1:
                enc = (unsigned char)((value & MASK7_DATA_0) | MASK7_CONT);
                out.push_back(enc);
                enc = (unsigned char)((value & MASK7_DATA_1)>>7);
                out.push_back(enc);
                break;
            case 2:
                enc = (unsigned char)((value & MASK7_DATA_0) | MASK7_CONT);
                out.push_back(enc);
                enc = ((unsigned char)((value & MASK7_DATA_1)>>7) | MASK7_CONT);
                out.push_back(enc);
                enc = (unsigned char)((value & MASK7_DATA_2)>>14);
                out.push_back(enc);
                break;
            case 3:
                enc = (unsigned char)((value & MASK7_DATA_0) | MASK7_CONT);
                out.push_back(enc);
                enc = ((unsigned char)((value & MASK7_DATA_1)>>7) | MASK7_CONT);
                out.push_back(enc);
                enc = ((unsigned char)((value & MASK7_DATA_2)>>14) | MASK7_CONT);
                out.push_back(enc);
                enc = (unsigned char)((value & MASK7_DATA_3)>>21);
                out.push_back(enc);
                break;
            default:
                assert (false);
        }

    }

}

void BAVE_dec(
        std::vector<unsigned int> & out,
        std::vector<unsigned char>& input
        )
{
    std::vector<unsigned char>::iterator itr = input.begin();
    std::vector<unsigned char>::iterator end = input.end();

    for (; itr != end; ++itr)
    {
        unsigned int val = 0;
        for(int cls = 0; ; ++cls, ++itr)
        {
            unsigned char enc = *itr;
            switch (cls)
            {
                case 0:
                    val = enc & MASK7_DATA_0;
                    break;
                case 1:
                    val = val | ((enc & MASK7_DATA_0) << 7);
                    break;
                case 2:
                    val = val | ((enc & MASK7_DATA_0) << 14);
                    break;
                case 3:
                    val = val | ((enc & MASK7_DATA_0) << 21);
                    break;
                default:
                    assert (false);
            }


            if (not (enc & MASK7_CONT))
            {
                out.push_back(val);
                //std::cout << val << ", " << cls << std::endl;
                break;
            }
        } // while

    } // for

}



void test_BAVE(int total_count)
{


    std::vector<unsigned int> input;
    std::vector<unsigned char> encrypted;
    std::vector<unsigned int> output;

    for (int i = 0; i < total_count; ++i)
    {
        input.push_back(500);
    }

    BAVE_enc(encrypted, input);

    output.reserve(total_count);

    struct timeval s, e;
    gettimeofday(&s, NULL);
    BAVE_dec(output, encrypted);
    gettimeofday(&e, NULL);
    double t = e.tv_sec * 1000000.0 + e.tv_usec - s.tv_sec * 1000000.0 - s.tv_usec;
    std::cout << "BAVE in usec:" << t << std::endl;
    std::cout << "BAVE in M#/sec:" << total_count/t << std::endl;


    std::vector<unsigned int>::iterator itr = output.begin();
    std::vector<unsigned int>::iterator end = output.end();
    for (int i = 0; itr != end; ++itr, ++i)
    {
        assert (*itr == input[i]);
    }

    std::cout << "compress ratio:" << float(encrypted.size())/(input.size()*4) << std::endl;
}


void test_GVE(int total_count)
{
    std::vector<unsigned int> input;
    std::vector<unsigned char> encrypted;
    std::vector<unsigned int> output;

    for (int i = 0; i < total_count; ++i)
    {
        input.push_back(500);
    }

    GVE_enc(encrypted, input);


    std::vector<DecPlan> dec_plan;
    gen_dec_plan(dec_plan);

    output.reserve(total_count);

    struct timeval s, e;
    gettimeofday(&s, NULL);
    GVE_dec(dec_plan, output, encrypted);
    gettimeofday(&e, NULL);
    double t = e.tv_sec * 1000000.0 + e.tv_usec - s.tv_sec * 1000000.0 - s.tv_usec;
    std::cout << "GVE in usec:" << t << std::endl;
    std::cout << "GVE in M#/sec:" << total_count/t << std::endl;


    std::vector<unsigned int>::iterator itr = output.begin();
    std::vector<unsigned int>::iterator end = output.end();
    for (int i = 0; itr != end; ++itr, ++i)
    {
        assert (*itr == input[i]);
    }

    std::cout << "compress ratio:" << float(encrypted.size())/(input.size()*4) << std::endl;
}

int main(int argc, char ** argv)
{
    int total_cnt = 10000000;
    test_BAVE(total_cnt);
    test_GVE(total_cnt);


    return 0;
}
