#include<iostream>
#include"balance.h"

int main(int argc, const char **argv)
{
    char filename[80];
    balance *p;
    int result;

    try
    {
        if (argc == 1)
        {
            std::cout << "Please provide the file path:\n";
            std::cin >> filename;
            p = new balance(filename);
            result = p->checkBalance();
            delete p;
            std::cout << result << " errors in all.\n";
            return 0;
        }
        while (--argc)
        {
            std::cout << "Checking file " << *++argv << '\n';
            p = new balance(*argv);
            result = p->checkBalance();
            delete p;
            std::cout << result << " errors in all.\n";
        }
    } catch (noFile) { std::cout << "no such file\n"; }
    return 0;
}