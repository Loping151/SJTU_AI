#include "gamebig.h"
#include "ui_mainbigwindow.h"

#include <random>
#include <iostream>
#include <vector>
#include <QDebug>
using namespace std;

GameBig::GameBig()
{
    initAll();
}

void GameBig::initAll()
{
    for(int i=0; i<BROW; i++)
    {
        for(int j=0; j<BCOL; j++)
        {
            data[i][j] = 0;
        }
    }
    gameStart = false;
    grade = 0;
    gradeBasic = 0;
    gradeUp = 0;
    step = -2;
    gradeUpCoefficient = 0;

    prob2 = 0;
    prob4 = 0;
    prob8 = 0;
    prob16 = 0;

    Colour_flag = -1;
    full = 0;
}

void GameBig::calProb()
{
    if(0.6 > gradeUpCoefficient)
    {
        prob2 = 100-gradeUpCoefficient*100*0.5;
        prob4 = 100;
        prob8 = 0;
        prob16 = 0;
    }
    else if(0.8 > gradeUpCoefficient)
    {
        prob2 = 100-(gradeUpCoefficient-0.4)*100*1.5;
        prob4 = 30+prob2;
        prob8 = 100;
        prob16 = 0;
    }
    else if(1 >= gradeUpCoefficient)
    {
        prob2 = 40-(gradeUpCoefficient-0.8)*100*0.5;
        prob4 = 30+prob2;
        prob8 = 30+prob4;
        prob16 = 100;
    }
}

void GameBig::createNum()
{
    vector<int> indexSpace;
    for(int i=0; i<BROW; i++)
    {
        for(int j=0; j<BCOL; j++)
        {
            if(!data[i][j])
            {
                indexSpace.push_back(i*5+j);
            }
        }
    }
    if(!indexSpace.empty())
    {
        int randNum = rand()%100;
        int randPlace = rand()%indexSpace.size();
        int chooseNum = -1;

        calProb();
        if     (prob2 > randNum)  chooseNum = 2;
        else if(prob4 > randNum)  chooseNum = 4;
        else if(prob8 > randNum)  chooseNum = 8;
        else if(prob16 > randNum) chooseNum = 16;
        int x = indexSpace[randPlace]/5;
        int y = indexSpace[randPlace]%5;
        Colour_flag = 5*x + y;
        data[x][y] = chooseNum;
        gradeUp += 2*chooseNum*gradeUpCoefficient;
        grade = gradeBasic + gradeUp;
        full = 0;
        step++;
    }
    else
        full = 1;
}

void GameBig::process(int cmd)
{
    switch(cmd)
    {
    case BCMD_UP:    moveUp();    break;
    case BCMD_DOWN:  moveDown();  break;
    case BCMD_LEFT:  moveLeft();  break;
    case BCMD_RIGHT: moveRight(); break;
    }
    createNum();
}

void GameBig::moveUp()
{
    for(int j=0; j<BCOL; j++)
    {
        int t[10] = {0};
        int cnt = 0;
        for(int i=0; i<BROW; i++)
            if(data[i][j])
                t[cnt++] = data[i][j];

        bool finish = 0;
        int zero = 0;
        while(!finish)
        {
            finish = 1;
            for(int k=0; k<cnt-1; k++)
            {
                zero = 0;
                while(t[k+zero+1]==0&&k+zero+1<3) zero++;
                if(t[k]==t[k+zero+1]&&t[k]!=0)
                {
                    finish = 0;
                    gradeBasic += t[k];
                    t[k] *= 2;
                    t[k+zero+1] = 0;
                    k+=zero;
                }
            }
        }

        int n = 0;
        for(int k=0; k<cnt; k++)
        {
            if(t[k])
                data[n++][j] = t[k];
        }

        for(; n<BROW; n++)
        {
            data[n][j] = 0;
        }
    }
}

void GameBig::moveDown()
{
    for(int j=0; j<BCOL; j++)
    {
        int t[10];
        int cnt = 0;

        for(int i=BROW-1; i>=0; i--)
            if(data[i][j])    t[cnt++] = data[i][j];

        bool finish = 0;
        int zero = 0;
        while(!finish)
        {
            finish = 1;
            for(int k=0; k<cnt-1; k++)
            {
                zero = 0;
                while(t[k+zero+1]==0&&k+zero+1<3) zero++;
                if(t[k]==t[k+zero+1]&&t[k]!=0)
                {
                    finish = 0;
                    gradeBasic += t[k];
                    t[k] *= 2;
                    t[k+zero+1] = 0;
                    k+=zero;
                }
            }
        }

        int n = BROW-1;
        for(int k=0; k<cnt; k++)
        {
            if(t[k])    data[n--][j] = t[k];
        }

        for(; n>=0; n--)
        {
            data[n][j] = 0;
        }
    }
}

void GameBig::moveLeft()
{
    for(int i=0; i<BROW; i++)
    {
        int t[10];
        int cnt = 0;
        for(int j=0; j<BCOL; j++)
            if(data[i][j])    t[cnt++] = data[i][j];

        bool finish = 0;
        int zero = 0;
        while(!finish)
        {
            finish = 1;
            for(int k=0; k<cnt-1; k++)
            {
                zero = 0;
                while(t[k+zero+1]==0&&k+zero+1<3) zero++;
                if(t[k]==t[k+zero+1]&&t[k]!=0)
                {
                    finish = 0;
                    gradeBasic += t[k];
                    t[k] *= 2;
                    t[k+zero+1] = 0;
                    k+=zero;
                }
            }
        }

        int n = 0;
        for(int k=0; k<cnt; k++)
        {
            if(t[k])    data[i][n++] = t[k];
        }

        for(; n<BCOL; n++)
        {
            data[i][n] = 0;
        }
    }
}

void GameBig::moveRight()
{
    for(int i=0; i<BROW; i++)
    {
        int t[10];
        int cnt = 0;
        for(int j=BCOL-1; j>=0; j--)
            if(data[i][j])    t[cnt++] = data[i][j];

        bool finish = 0;
        int zero = 0;
        while(!finish)
        {
            finish = 1;
            for(int k=0; k<cnt-1; k++)
            {
                zero = 0;
                while(t[k+zero+1]==0&&k+zero+1<3) zero++;
                if(t[k]==t[k+zero+1]&&t[k]!=0)
                {
                    finish = 0;
                    gradeBasic += t[k];
                    t[k] *= 2;
                    t[k+zero+1] = 0;
                    k+=zero;
                }
            }
        }

        int n = BCOL-1;
        for(int k=0; k<cnt; k++)
        {
            if(t[k])    data[i][n--] = t[k];
        }

        for(; n>=0; n--)
        {
            data[i][n] = 0;
        }
    }
}

void GameBig::clear()
{
    int min = 1024;
    for (int i=0; i<BROW; i++)
    {
        for (int j=0; j<BCOL; j++)
        {
            if (data[i][j]<min&&data[i][j]!=0)
                min = data[i][j];
        }
    }

    for (int i=0; i<BROW; i++)
    {
        for (int j=0; j<BCOL; j++)
        {
            if (data[i][j]==min)
                data[i][j] = 0;
        }
    }
}

void GameBig::cheat()
{
    for (int i=0; i<BROW; i++)
    {
        for (int j=0; j<BCOL; j++)
        {
            if(data[i][j]!=0)
                data[i][j] = 1024;
        }
    }
}

int GameBig::judge()
{
    for (int i=0; i<BROW; i++)
    {
        for (int j=0; j<BCOL; j++)
        {
            if (data[i][j] >= 4096)
            {
                return BSTAT_WIN;
            }
        }
    }

    for (int i=0; i<BROW; i++)
    {
        for (int j=0; j<BCOL-1; j++)
        {
            if (!data[i][j] || (data[i][j] == data[i][j+1]) || !data[i][3])//因为下标对不上，所以需要补充末行末列
            {
                return BSTAT_PROCESS;
            }
        }
    }

    for (int j=0; j<BCOL; j++)
    {
        for (int i=0; i<BROW-1; i++)
        {
            if (!data[i][j] || (data[i][j] == data[i+1][j]) || !data[3][j])
            {
                return BSTAT_PROCESS;
            }
        }
    }

    gameStart = false;
    return BSTAT_LOSE;
}

bool GameBig::getGameStart(){return gameStart;}
void GameBig::setGameStart(bool flag){gameStart = flag;}
void GameBig::setGradeUpCoefficient(float i){gradeUpCoefficient = i;}
int GameBig::getData(int i, int j){return data[i][j];}
int GameBig::getGrade(){return grade;}
int GameBig::getGradeBasic(){return gradeBasic;}
int GameBig::getGradeUp(){return gradeUp;}
int GameBig::getStep(){return step;}
int GameBig::getColour(){return Colour_flag;}
bool GameBig::getFull(){return full;}
