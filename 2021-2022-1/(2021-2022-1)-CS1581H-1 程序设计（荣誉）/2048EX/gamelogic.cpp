#include "gamelogic.h"
#include "ui_mainwindow.h"

#include <random>
#include <iostream>
#include <vector>
#include <QDebug>
using namespace std;

//构造函数,调用初始化函数初始化
GameLogic::GameLogic()
{
    initAll();
}

//各项数据初始化单独作为函数，便于重开
void GameLogic::initAll()
{
    for(int i=0; i<ROW; i++)
    {
        for(int j=0; j<COL; j++)
        {
            data[i][j] = 0;
        }
    }
    gameStart = false;
    grade = 0;
    gradeBasic = 0;
    gradeUp = 0;
    step = -2;//因为后面把这个和生成绑定了,所以初始应该是-2
    gradeUpCoefficient = 0;

    prob2 = 0;
    prob4 = 0;
    prob8 = 0;
    prob16 = 0;

    colour_flag = -1;//坐标范围是0到15
    full = 0;
}

//规定难度梯度,计算各个数字生成概率
void GameLogic::calProb()
{
    //qDebug() << "gradeUpCoefficient:" << gradeUpCoefficient ;
    if(0.6 > gradeUpCoefficient) //第一阶段，包括前三个等级，只生成2和4，其中最简单的只生成2，难度提升后就是出现的数字种类更多，而且更加平均
    {
        prob2 = 100-gradeUpCoefficient*100*0.5;         // 100%->70%
        prob4 = 100;                                    // 0%->30%
        prob8 = 0;                                      // 0%
        prob16 = 0;                                     // 0%
        //qDebug() << "2:" << prob2 << " 4:" << prob4 << " 8:" << prob8 << " 16:" << prob16 ;
    }
    else if(0.8 > gradeUpCoefficient) // 0.6->0.8 高手级 新增8
    {
        prob2 = 100-(gradeUpCoefficient-0.4)*100*1.5;   // 70%->40%
        prob4 = 30+prob2;                               // 30%
        prob8 = 100;                                    // 0%->30%
        prob16 = 0;                                     // 0%
        //qDebug() << "2:" << prob2 << " 4:" << prob4 << " 8:" << prob8 << " 16:" << prob16 ;
    }
    else if(1 >= gradeUpCoefficient) // 0.8->1.0 巨佬级 新增16
    {
        prob2 = 40-(gradeUpCoefficient-0.8)*100*0.5;    // 40%->30%
        prob4 = 30+prob2;                               // 30%
        prob8 = 30+prob4;                               // 30%
        prob16 = 100;                                   // 0%->10%
        //qDebug() << "2:" << prob2 << " 4:" << prob4 << " 8:" << prob8 << " 16:" << prob16 ;
    }
}

//生成一个数字
void GameLogic::createNum()
{
    vector<int> indexSpace;//新建空容器
    for(int i=0; i<ROW; i++)
    {
        for(int j=0; j<COL; j++)
        {
            if(!data[i][j])
            {
                indexSpace.push_back(i*4+j);//如果位置是空的,就在容器中记录序数
            }
        }
    }
    if(!indexSpace.empty())//判断是否为空,即棋盘是否布满
    {
        int randNum = rand()%100;
        int randPlace = rand()%indexSpace.size();
        int chooseNum = -1;

        calProb();//更新难度
        //qDebug() << "randNum:" << randNum;
        //qDebug() << "2:" << prob2 << " 4:" << prob4 << " 8:" << prob8 << " 16:" << prob16 ;
        if     (prob2 > randNum)  chooseNum = 2;//产生数字
        else if(prob4 > randNum)  chooseNum = 4;
        else if(prob8 > randNum)  chooseNum = 8;
        else if(prob16 > randNum) chooseNum = 16;
        int x = indexSpace[randPlace]/4;//放置在空位置
        int y = indexSpace[randPlace]%4;
        //qDebug("x%dx y%d"y,x,y);
        colour_flag = 4*x + y;
        data[x][y] = chooseNum;//新添数字
        gradeUp += 2*chooseNum*gradeUpCoefficient;//加成分数:产生数字的两倍乘以百分比
        grade = gradeBasic + gradeUp;
        full = 0;
        step++;
    }
    else
        full = 1;
}

//操作过程
void GameLogic::process(int cmd)
{
    switch(cmd)
    {
    case CMD_UP:    moveUp();    break;
    case CMD_DOWN:  moveDown();  break;
    case CMD_LEFT:  moveLeft();  break;
    case CMD_RIGHT: moveRight(); break;
    }
    createNum();
}

//上移操作
void GameLogic::moveUp()
{
    for(int j=0; j<COL; j++)
    {
        //对于每一列
        int t[10] = {0};
        int cnt = 0;
        for(int i=0; i<ROW; i++)
            if(data[i][j])
                t[cnt++] = data[i][j];//如果发现非零元素，计数并存放

        bool finish = 0;
        int zero = 0;//计算0的数目
        while(!finish)
        {
            finish = 1;
            for(int k=0; k<cnt-1; k++)//在存放数列中合并相同项并加倍
            {
                zero = 0;
                while(t[k+zero+1]==0&&k+zero+1<3) zero++;//如果发现0，就跳过
                if(t[k]==t[k+zero+1]&&t[k]!=0)
                {
                    finish = 0;//排序未完成
                    gradeBasic += t[k];//基准分计算方法就是合并的数字和
                    t[k] *= 2;
                    t[k+zero+1] = 0;
                    k+=zero;//跳过的0,没必要再算
                }
            }
        }
        //将合并后的非零元素填入data中
        int n = 0;
        for(int k=0; k<cnt; k++)
        {
            if(t[k])
                data[n++][j] = t[k];
        }
        //尾部补零
        for(; n<ROW; n++)
        {
            data[n][j] = 0;
        }
    }
}

void GameLogic::moveDown()
{
    for(int j=0; j<COL; j++)
    {
        int t[10];
        int cnt = 0;

        for(int i=ROW-1; i>=0; i--)
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

        int n = ROW-1;
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

void GameLogic::moveLeft()
{
    for(int i=0; i<ROW; i++)
    {
        int t[10];
        int cnt = 0;
        for(int j=0; j<COL; j++)
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

        for(; n<COL; n++)
        {
            data[i][n] = 0;
        }
    }
}

void GameLogic::moveRight()
{
    for(int i=0; i<ROW; i++)
    {
        int t[10];
        int cnt = 0;
        for(int j=COL-1; j>=0; j--)
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

        int n = COL-1;
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

void GameLogic::clear()
{
    int min = 1024;
    for (int i=0; i<ROW; i++)//擂台法检索最小值,反正也就16个数字
    {
        for (int j=0; j<COL; j++)
        {
            if (data[i][j]<min&&data[i][j]!=0)
                min = data[i][j];
        }
    }

    for (int i=0; i<ROW; i++)//清除这些数字
    {
        for (int j=0; j<COL; j++)
        {
            if (data[i][j]==min)
                data[i][j] = 0;
        }
    }
}

void GameLogic::cheat()
{
    for (int i=0; i<ROW; i++)//把所有现有数字变为1024,其意义是方便了作者看到赢了会发生什么.写于AI产生之前
    {
        for (int j=0; j<COL; j++)
        {
            if(data[i][j]!=0)
                data[i][j] = 1024;
        }
    }
}

int GameLogic::judge()
{
    //赢了
    for (int i=0; i<ROW; i++)
    {
        for (int j=0; j<COL; j++)
        {
            if (data[i][j] >= 2048)//注意是大于等于,不排除手速过快直接产生4096的玩家
            {
                return STAT_WIN;
            }
        }
    }
    //横向存活
    for (int i=0; i<ROW; i++)
    {
        for (int j=0; j<COL-1; j++)
        {
            if (!data[i][j] || (data[i][j] == data[i][j+1]) || !data[i][3])//因为下标对不上，所以需要补充末行末列
            {
                return STAT_PROCESS;
            }
        }
    }
    //纵向存活
    for (int j=0; j<COL; j++)
    {
        for (int i=0; i<ROW-1; i++)
        {
            if (!data[i][j] || (data[i][j] == data[i+1][j]) || !data[3][j])
            {
                return STAT_PROCESS;
            }
        }
    }
    //其他情况,包括某些没修复的bug(至少我发现的都修了)
    gameStart = false;
    return STAT_LOSE;
}

//获取函数
bool GameLogic::getGameStart(){return gameStart;}
void GameLogic::setGameStart(bool flag){gameStart = flag;}
void GameLogic::setGradeUpCoefficient(float i){gradeUpCoefficient = i;}
int GameLogic::getData(int i, int j){return data[i][j];}
int GameLogic::getGrade(){return grade;}
int GameLogic::getGradeBasic(){return gradeBasic;}
int GameLogic::getGradeUp(){return gradeUp;}
int GameLogic::getStep(){return step;}
int GameLogic::getColour(){return colour_flag;}
bool GameLogic::getFull(){return full;}
