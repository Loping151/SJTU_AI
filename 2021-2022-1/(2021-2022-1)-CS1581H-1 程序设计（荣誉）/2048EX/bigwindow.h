#ifndef BIGWINDOW_H
#define BIGWINDOW_H

#include <QMainWindow>
#include <QKeyEvent>
#include <QDebug>
#include <QMessageBox>
#include <QTextBrowser>
#include <QTime>

#include "gamebig.h"

namespace Ui {
class BigWindow;
}

class BigWindow : public QMainWindow
{
    Q_OBJECT

public:
    GameBig* game;
    explicit BigWindow(QWidget *parent = 0);
    ~BigWindow();
    void initAll();
    void showMessage();
    void showBroad();
    void keyPressEvent(QKeyEvent *event);
    void changeColor(QLabel* label, int num);
    void changeColorSlide(QLabel* label);
    void Sleep(int msec);
    void showRule();
    void closeEvent(QCloseEvent *);

signals:
    void ExitWin();

private slots:
    void on_pushButton_start_clicked();

    void on_pushButton_close_clicked();

    void on_horizontalSlider_valueChanged(int value);

    void on_pushButton_show_clicked();

    void on_pushButton_clear_clicked();

    void on_pushButton_cheat_clicked();

    void on_pushButton_AI_clicked();

    void on_pushButton_change_clicked();

private:
    Ui::BigWindow *ui;
    int message_count[2]{};
    int sleepTime;
    bool blinking;
    bool AIrun;
};

#endif // BigWindow_H
