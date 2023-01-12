#ifndef GAMELOGIC_H
#define GAMELOGIC_H

#include <iostream>
const int ROW = 4;
const int COL = 4;

enum CMD
{
    CMD_UP,
    CMD_DOWN,
    CMD_LEFT,
    CMD_RIGHT,
};

enum STAT
{
    STAT_WAIT,
    STAT_PROCESS,
    STAT_WIN,
    STAT_LOSE,
};

class GameLogic
{
public:
    GameLogic();//构造函数
    void createNum();//生成
    void process(int cmd);//每个步骤
    int judge();//判断状态函数
    void initAll();//初始化函数
    void calProb();//召唤概率

    void moveUp();//上移
    void moveDown();//下移
    void moveLeft();//左移
    void moveRight();//右移

    bool getGameStart();//都是获取函数
    bool getFull();
    void setGameStart(bool);
    void setGradeUpCoefficient(float);
    int getData(int,int);
    int getGrade();
    int getGradeBasic();
    int getGradeUp();
    int getStep();
    int getColour();

    void clear();//作弊函数
    void cheat();//作弊函数

private:
    bool gameStart;//游戏开始状态
    int data[ROW][COL];//棋盘
    float grade;//分数
    int gradeBasic;//基准分
    float gradeUp;//奖励分
    int step;//步数
    float gradeUpCoefficient;//加成比例
    int prob2;//各个数字的概率
    int prob4;//同上
    int prob8;//同上
    int prob16;//同上
    int colour_flag;//变色坐标
    int full;//满没满
};

#endif // GAMELOGIC_H
