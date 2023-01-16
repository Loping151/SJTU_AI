//
// Created by Kailing Wang on 2022/3/3.
//

#ifndef STACK_BALANCE_H
#define STACK_BALANCE_H

#include "seqStack.h"
#include "seqStack.cpp"
#include <fstream>
#include <iostream>

class balance
{
private:
    std::ifstream fin;
    int currentLine;
    int errors;

    struct Symbol
    {
        char token;
        int theLine;
    };
    enum CommentType
    {
        slashSlash,
        slashStar
    };

    static bool checkMatch(char symbol1, char symbol2, int line1, int line2);

    char getNextSymbol();

    void putBackChar(char ch);

    void skipComment(enum CommentType type);

    void skipQuote(char type);

    char nextChar();

public:
    explicit balance(const char *);

    int checkBalance();
};

class noFile
{
};

#endif // STACK_BALANCE_H
