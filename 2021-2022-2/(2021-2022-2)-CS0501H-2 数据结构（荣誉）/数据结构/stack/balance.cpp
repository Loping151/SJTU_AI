//
// Created by Kailing Wang on 2022/3/3.
//

#include "balance.h"

balance::balance(const char *s)
{
    fin.open(s);
    if (not fin)throw noFile();

    currentLine = 1;
    errors = 0;
}

int balance::checkBalance()
{
    Symbol node{};
    seqStack<Symbol> st;
    char lastChar, match;
    while ((lastChar = getNextSymbol()))
    {
        switch (lastChar)
        {
            case '(':
            case '[':
            case '{':
                node.token = lastChar;
                node.theLine = currentLine;
                st.push(node);
                break;
            case ')':
            case ']':
            case '}':
                if (st.isEmpty())
                {
                    ++errors;
                    std::cout << "In line " << currentLine << " there is a 多余的" << lastChar << '\n';
                }
                else
                {
                    node = st.pop();
                    match = node.token;
                    if (not checkMatch(match, lastChar, node.theLine, currentLine))
                        ++errors;
                }
                break;
        }
    }
    while (not st.isEmpty())
    {
        ++errors;
        node = st.pop();
        std::cout << "In line " << node.theLine << " there is a " << node.token << "不匹配\n";
    }
    return errors;
}

bool balance::checkMatch(char symbol1, char symbol2, int line1, int line2)
{
    if (symbol1 == '(' and symbol2 not_eq ')' or symbol1 == '[' and symbol2 not_eq ']' or symbol1 == '{' and
        symbol2 not_eq '}')
    {
        std::cout << "Found " << symbol1 << " in line " << line1 << " not match with " << symbol2 << "in" << line2;
        return false;
    }
    else return true;
}

char balance::getNextSymbol()
{
    char ch;
    while ((ch = nextChar()))
    {
        if (ch == '/')
        {
            ch = nextChar();
            if (ch == '*')skipComment(slashStar);
            else if (ch == '/')skipComment(slashSlash);
            else putBackChar(ch);
        }
        else if (ch == '\'' or ch == '\"')
            skipQuote(ch);
        else if (ch == '{' or ch == '[' or ch == '(' or ch == ')' or ch == ']' or ch == '}')
            return ch;
    }
    return '\0';
}

char balance::nextChar()
{
    char ch;
    if ((ch = fin.get()) == EOF)return '\0';
    if (ch == '\n')++currentLine;
    return ch;
}


void balance::putBackChar(char ch)
{
    fin.putback(ch);
    if (ch == '\n')
        --currentLine;
}

void balance::skipQuote(char type)
{
    char ch;
    while ((ch = nextChar()))
    {
        if (ch == type)return;
        else if (ch == '\n')
        {
            ++errors;
            std::cout << "Missing closing quote at line\n";
        }
        else if (ch == '\\')ch = nextChar();
    }
}

void balance::skipComment(enum CommentType type)
{
    char ch, flag = 0;

    if (type == slashSlash)
        while ((ch = nextChar()) not_eq '\0')
        {
            if (flag == '*' and ch == '/')return;
            flag = ch;
        }
    ++errors;
    std::cout << "Comment is unterminated!\n";
}