#include "bigwindow.h"
#include "ui_mainbigwindow.h"

BigWindow::BigWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::BigWindow)
{
    game = new GameBig;
    blinking = true;
    AIrun = false;
    sleepTime = 100;
    ui->setupUi(this);
    showBroad();
}

BigWindow::~BigWindow()
{
    delete ui;
}

void BigWindow::initAll()
{
    game->initAll();
    on_horizontalSlider_valueChanged(ui->horizontalSlider->value());
}

void BigWindow::on_pushButton_start_clicked()
{
    ui->pushButton_start->setText("重开");
    initAll();

    game->setGameStart(true);

    blinking = true;
    AIrun = false;

    ui->pushButton_start->setEnabled(false);//暂时禁用按钮 防止连按产生bug
    ui->pushButton_close->setEnabled(false);
    ui->pushButton_cheat->setEnabled(false);
    ui->pushButton_clear->setEnabled(false);
    ui->pushButton_change->setEnabled(false);
    ui->pushButton_AI->setEnabled(false);

    game->createNum();
    showBroad();
    Sleep(300);
    game->createNum();
    showBroad();
    ui->pushButton_start->setEnabled(true);
    ui->pushButton_close->setEnabled(true);
    ui->pushButton_cheat->setEnabled(true);
    ui->pushButton_clear->setEnabled(true);
    ui->pushButton_change->setEnabled(true);
    ui->pushButton_AI->setEnabled(true);

    showMessage();
}

void BigWindow::on_pushButton_close_clicked()
{
    this->close();
}

void BigWindow::on_horizontalSlider_valueChanged(int value)
{
    value = ui->horizontalSlider->value();
    ui->label_showGradeUpCoefficient->setText(QString::number(value*2)+"%");
    game->setGradeUpCoefficient((float)ui->horizontalSlider->value()/100);

    if(0 == value) ui->label_showDifficult->setText("菜鸟");
    else if(20 > value)  ui->label_showDifficult->setText("萌新");
    else if(40 > value)  ui->label_showDifficult->setText("入门");
    else if(60 > value)  ui->label_showDifficult->setText("普通");
    else if(80 > value)  ui->label_showDifficult->setText("高手");
    else if(100 > value) ui->label_showDifficult->setText("巨佬");
    else ui->label_showDifficult->setText("这也能卷？");
}

void BigWindow::on_pushButton_show_clicked()
{
    showRule();
}

void BigWindow::on_pushButton_clear_clicked()
{
    if(game->getGameStart())
    {
        game->clear();
        blinking = false;
        showBroad();
        blinking = true;
    }
}

void BigWindow::on_pushButton_cheat_clicked()
{

    if(game->getGameStart())
    {
        game->cheat();
        blinking = false;
        showBroad();
        blinking = true;
    }
}

void BigWindow::on_pushButton_AI_clicked()
{
    AIrun = !AIrun;
    if(AIrun)
    {
        sleepTime = 0;
        ui->pushButton_close->setEnabled(false);
        ui->pushButton_cheat->setEnabled(false);
        ui->pushButton_clear->setEnabled(false);
        ui->pushButton_change->setEnabled(false);

        int AI_step;
        while(game->getGameStart())
        {
            ui->pushButton_start->setEnabled(false);
            if(!AIrun)
            {
                break;
                sleepTime = 100;
            }
            srand(97*clock());
            if (AI_step == rand()%4)
                AI_step = 3 - AI_step;
            else
            {
                AI_step = rand()%4;
            }

            switch(AI_step)
            {
            case 0:  game->process(BCMD_UP);    break;
            case 1:  game->process(BCMD_DOWN);  break;
            case 2:  game->process(BCMD_LEFT);  break;
            case 3:  game->process(BCMD_RIGHT); break;
            }
            showMessage();
            switch(game->judge())
            {
            case BSTAT_PROCESS:showBroad(); break;
            case BSTAT_WIN:
                showBroad();
                blinking = 0;
                blinking = true;
                AIrun = false;
                sleepTime = 100;
                QMessageBox::information(NULL,"4096","不劳而获的感觉咋样?");
                game->setGameStart(false);
                break;
            case BSTAT_LOSE:
                game->clear();
                game->clear();
                game->setGameStart(true);
            }
            Sleep(15);
        }
    }

    ui->pushButton_start->setEnabled(true);
    ui->pushButton_close->setEnabled(true);
    ui->pushButton_cheat->setEnabled(true);
    ui->pushButton_clear->setEnabled(true);
    ui->pushButton_change->setEnabled(true);
    sleepTime = 100;
}

void BigWindow::on_pushButton_change_clicked()
{
    this->close();
}

void BigWindow::keyPressEvent(QKeyEvent *event)
{
    if(ui->pushButton_start->isEnabled()&&game->getGameStart())
    {
        switch(event->key())
        {
        case Qt::Key_Up: case Qt::Key_W:    game->process(BCMD_UP);    break;
        case Qt::Key_Down: case Qt::Key_S:  game->process(BCMD_DOWN);  break;
        case Qt::Key_Left: case Qt::Key_A:  game->process(BCMD_LEFT);  break;
        case Qt::Key_Right: case Qt::Key_D: game->process(BCMD_RIGHT); break;
        default: break;
        }
        showMessage();
        switch(game->judge())
        {
        case BSTAT_PROCESS:showBroad(); break;
        case BSTAT_WIN:
            showBroad();
            blinking = 0;
            if(game->getGameStart())
            {
                QMessageBox::information(NULL,"4096","以为这就赢了?");
                QMessageBox::information(NULL,"4096","好吧,确实");
                blinking = true;
                game->setGameStart(false);
            }
            break;
        case BSTAT_LOSE:
            showBroad();
            blinking = 0;
            QMessageBox::information(NULL,"4096","不会吧不会吧.不会这都有人赢不了吧"); break;
        }
    }
}

void BigWindow::showMessage()
{
    ui->label_showGrade->setText(QString::number(game->getGrade()));
    ui->label_showGradeBasic->setText(QString::number(game->getGradeBasic()));
    ui->label_showGradeUp->setText(QString::number(game->getGradeUp()));
    ui->label_showStep->setText(QString::number(game->getStep()));
}

void BigWindow::showBroad()
{
    for(int i = 0;i < BROW;i++)
    {
        for(int j = 0;j < BCOL;j++)
        {
            if(game->getData(i,j)) findChild<QLabel *>("label_"+QString::number(i)+QString::number(j))->setText(QString::number(game->getData(i,j)));
            else                   findChild<QLabel *>("label_"+QString::number(i)+QString::number(j))->setText(" ");
            changeColor(findChild<QLabel *>("label_"+QString::number(i)+QString::number(j)), game->getData(i,j));
        }
    }
    if(game->getColour()!=-1&&game->getGameStart()&&blinking&&!game->getFull())
    {
        blinking = false;
        Sleep(sleepTime);
        changeColorSlide(findChild<QLabel *>("label_"+QString::number(game->getColour()/5)+QString::number(game->getColour()%5)));
        Sleep(sleepTime);
        changeColor(findChild<QLabel *>("label_"+QString::number(game->getColour()/5)+QString::number(game->getColour()%5)), game->getData(game->getColour()/5,game->getColour()%5));
        blinking = true;
        Sleep(sleepTime);
        changeColorSlide(findChild<QLabel *>("label_"+QString::number(game->getColour()/5)+QString::number(game->getColour()%5)));
        Sleep(sleepTime);
        changeColor(findChild<QLabel *>("label_"+QString::number(game->getColour()/5)+QString::number(game->getColour()%5)), game->getData(game->getColour()/5,game->getColour()%5));
    }
}

void BigWindow::changeColor(QLabel* label, int num)
{
    label->setAlignment(Qt::AlignCenter);
    switch (num)
    {
    case 2:    label->setStyleSheet("background-color: rgb(238,228,218);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 4:    label->setStyleSheet("background-color: rgb(237,224,200);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 8:    label->setStyleSheet("background-color: rgb(242,177,121);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 16:   label->setStyleSheet("background-color: rgb(245,150,100);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 32:   label->setStyleSheet("background-color: rgb(245,125,95);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 64:   label->setStyleSheet("background-color: rgb(245,95,60);"
                                    "font:bold 75 30pt ""微软雅黑"""); break;
    case 128:  label->setStyleSheet("background-color: rgb(237,207,114);"
                                    "font:bold 75 25pt ""微软雅黑"""); break;
    case 256:  label->setStyleSheet("background-color: rgb(237,204,97);"
                                    "font:bold 75 25pt ""微软雅黑"""); break;
    case 512:  label->setStyleSheet("background-color: rgb(237,204,97);"
                                    "font:bold 75 25pt ""微软雅黑"""); break;
    case 1024: label->setStyleSheet("background-color: rgb(237,204,97);"
                                    "font:bold 75 20pt ""微软雅黑"""); break;
    case 2048: label->setStyleSheet("background-color: rgb(237,210,70);"
                                    "font:bold 75 20pt ""微软雅黑"""); break;
    case 4096: label->setStyleSheet("background-color: rgb(237,180,100);"
                                    "font:bold 75 20pt ""微软雅黑"""); break;
    case 8192: label->setStyleSheet("background-color: rgb(237,180,100);"
                                    "font:bold 75 20pt ""微软雅黑"""); break;
    case 16384: label->setStyleSheet("background-color: rgb(237,180,100);"
                                     "font:bold 75 15pt ""微软雅黑"""); break;
    case 32768: label->setStyleSheet("background-color: rgb(237,180,100);"
                                     "font:bold 75 15pt ""微软雅黑"""); break;
    default:   label->setStyleSheet("background-color: rgb(238,228,218);"
                                    "font:bold 75 40pt ""微软雅黑"""); break;
    }
}

void BigWindow::changeColorSlide(QLabel* label)
{
    label->setStyleSheet("background-color: rgb(255,0,0);""font:bold 75 30pt ""微软雅黑""");
}

void BigWindow::Sleep(int msec)
{
    QTime dieTime = QTime::currentTime().addMSecs(msec);
    while( QTime::currentTime() < dieTime )
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
}

void BigWindow::showRule()
{
    QMessageBox::information(NULL,"4096","现在告知游戏规则：\n\n");
    QMessageBox::information(NULL,"4096","4096游戏：\n用方向键控制，\n合并数字，到达4096，");
    QMessageBox::information(NULL,"4096","右边显示了你的得分，\n等于合并过的数字之和\n加上产生数字乘以加成比例");
    QMessageBox::information(NULL,"4096","难度和数字产生概率相关,\n越高的等级产生的数字越随机\n");
    QMessageBox::information(NULL,"4096","你也许从未到达过4096,\n所以我赐予你神的力量:\n");
    QMessageBox::information(NULL,"4096","使用星辰之力,\n将所有2的最低次项化为星削\n");
    QMessageBox::information(NULL,"4096","你还可以使用            \n极     为    先    进\n的AI托管功能          ");
    QMessageBox::information(NULL,"4096","如果你忘记了我说的,\n点击右下角的查看教程\n欢迎随时回来");
    QMessageBox::information(NULL,"4096","现在,开始吧\n一旦开始,\n就请不要轻易放弃       ");
}

void BigWindow::closeEvent(QCloseEvent *)
{
    emit ExitWin();
}
