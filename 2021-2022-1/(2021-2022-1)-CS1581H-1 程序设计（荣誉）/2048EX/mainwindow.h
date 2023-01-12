#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QKeyEvent>
#include <QDebug>
#include <QMessageBox>
#include <QTextBrowser>
#include <QTime>

#include "gamelogic.h"
#include "bigwindow.h"

enum MESSAGE
{
    MESSAGE_ROLL,
    MESSAGE_QUIT,
};

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    GameLogic* game;
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void initAll();//窗口初始化
    void showMessage();//刷新数据
    void showBroad();//刷新棋盘
    void keyPressEvent(QKeyEvent *event);//键盘交互
    void changeColor(QLabel* label, int num);//刷新颜色
    void changeColorSlide(QLabel* label);//颜色闪烁,本来打算实现渐变,后来发现闪烁更好
    void Sleep(int msec);//待命函数
    void showRule();//显示规则

private slots:
    void on_pushButton_start_clicked();//都是按钮行为函数

    void on_pushButton_close_clicked();

    void on_horizontalSlider_valueChanged(int value);

    void on_pushButton_show_clicked();

    void on_pushButton_clear_clicked();

    void on_pushButton_cheat_clicked();

    void on_pushButton_AI_clicked();

    void on_pushButton_change_clicked();

private:
    Ui::MainWindow *ui;
    BigWindow *bigw;
    int message_count[2]{};
    int sleepTime;//待命时间
    bool blinking;//闪烁效果开关,修复了闪烁效果可以叠加的bug
    bool rule;//修复了作者每次测试都要自己看一遍规则的bug
    bool AIrun;//AI状态开关,自己想到最朴素的方法实现了按钮重按开关功能
};

#endif // MAINWINDOW_H
