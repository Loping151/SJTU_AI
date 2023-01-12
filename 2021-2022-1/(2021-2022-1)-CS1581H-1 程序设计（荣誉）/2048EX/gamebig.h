#ifndef GAMEBIG_H
#define GAMEBIG_H

#include <iostream>
const int BROW = 5;//change
const int BCOL = 5;//change

enum BCMD
{
    BCMD_UP,
    BCMD_DOWN,
    BCMD_LEFT,
    BCMD_RIGHT,
};

enum BSTAT
{
    BSTAT_WAIT,
    BSTAT_PROCESS,
    BSTAT_WIN,
    BSTAT_LOSE,
};

class GameBig
{
public:
    GameBig();
    void createNum();
    void process(int cmd);
    int judge();
    void initAll();
    void calProb();

    void moveUp();
    void moveDown();
    void moveLeft();
    void moveRight();

    bool getGameStart();
    bool getFull();
    void setGameStart(bool);
    void setGradeUpCoefficient(float);
    int getData(int,int);
    int getGrade();
    int getGradeBasic();
    int getGradeUp();
    int getStep();
    int getColour();

    void clear();
    void cheat();

private:
    bool gameStart;
    int data[BROW][BCOL];
    float grade;
    int gradeBasic;
    float gradeUp;
    int step;
    float gradeUpCoefficient;
    int prob2;
    int prob4;
    int prob8;
    int prob16;
    int Colour_flag;
    int full;
};

#endif // GAMELOGIC_H
