#include "mainwindow.h"
#include "ui_mainwindow.h"

//构造
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    game = new GameLogic;
    blinking = true;
    rule = false;
    AIrun = false;
    sleepTime = 100;
    ui->setupUi(this);
    showBroad();
}

//析构函数
MainWindow::~MainWindow()
{
    delete ui;
}

//初始化游戏逻辑对象
void MainWindow::initAll()
{
    game->initAll();
    on_horizontalSlider_valueChanged(ui->horizontalSlider->value());
}

//当登入被点击
void MainWindow::on_pushButton_start_clicked()
{
    ui->pushButton_start->setText("重开");
    initAll();//重新初始化

    if(!rule)//消息窗口,避免了作者每次看教程
    {
        QMessageBox * mBox = new QMessageBox(this);
        mBox->setWindowTitle("2048");
        mBox->setText("是否查看教程?");
        mBox->setStandardButtons(QMessageBox::StandardButton::Ok | QMessageBox::StandardButton::Cancel);
        mBox->setButtonText(QMessageBox::StandardButton::Ok, "是");
        mBox->setButtonText(QMessageBox::StandardButton::Cancel, "否");
        mBox->exec();
        QMessageBox::StandardButton ret = mBox->standardButton(mBox->clickedButton());
        switch (ret)
        {
        case QMessageBox::NoButton:
            rule = false;
            break;
        case QMessageBox::Ok:
            rule = false;
            break;
        case QMessageBox::Cancel:
            rule = true;
            break;
        default:
            break;
        }
        if (mBox != nullptr)
        {
            delete mBox;
            mBox = nullptr;
        }
    }

    if(!rule)//如果选择是,显示教程
    {
        showRule();
        rule = true;
    }

    game->setGameStart(true);//游戏设置开始,初始化值是false

    blinking = true;
    AIrun = false;

    ui->pushButton_start->setEnabled(false);//暂时禁用按钮 防止连按产生bug
    ui->pushButton_close->setEnabled(false);//我发现,禁用实在是行之有效,避免了巨多bug
    ui->pushButton_cheat->setEnabled(false);
    ui->pushButton_clear->setEnabled(false);
    ui->pushButton_change->setEnabled(false);
    ui->pushButton_AI->setEnabled(false);

    game->createNum();//产生数字
    showBroad();//刷新,闪一闪
    Sleep(300);//待命,看着更高级一点
    game->createNum();//再产生一个数字
    showBroad();//重复

    ui->pushButton_start->setEnabled(true);//取消禁用
    ui->pushButton_close->setEnabled(true);
    ui->pushButton_cheat->setEnabled(true);
    ui->pushButton_clear->setEnabled(true);
    ui->pushButton_change->setEnabled(true);
    ui->pushButton_AI->setEnabled(true);

    showMessage();//开启面板
}

//当登出被点击
void MainWindow::on_pushButton_close_clicked()
{
    switch(message_count[MESSAGE_QUIT])//登出按钮的花样,一共有7个事件,本来还想搞随机的,就这个MESSAGE系列,后来发现喧宾夺主了
    {
    case 0:
        QMessageBox::information(NULL,"2048","不可以轻易放弃哦");
        message_count[MESSAGE_QUIT]++;
        break;
    case 1:
        QMessageBox::information(NULL,"2048","还想登出呢?\n当年桐姥爷有登出吗?");
        message_count[MESSAGE_QUIT]++;
        ui->pushButton_close->setEnabled(false);//暂时禁用按钮
        Sleep(3000);
        ui->pushButton_close->setEnabled(true);
        break;
    case 2:
        QMessageBox::information(NULL,"2048","我说过不能退出了吧\n你听不懂是不是?");
        message_count[MESSAGE_QUIT]++;
        break;
    case 3:
        ui->pushButton_close->move(QPoint(520, 290));
        message_count[MESSAGE_QUIT]++;
        break;
    case 4:
        ui->pushButton_close->move(QPoint(670, 290));
        message_count[MESSAGE_QUIT]++;
        break;
    case 5:
        ui->pushButton_close->move(QPoint(600, 290));
        message_count[MESSAGE_QUIT]++;
        break;
    case 6:
        QMessageBox::information(NULL,"2048","算了,不为难你了");
        message_count[MESSAGE_QUIT] = 0;
        this->close();
        break;
    }
}

void MainWindow::on_horizontalSlider_valueChanged(int value)
{
    value = ui->horizontalSlider->value();//读取滑动条子,并且计算分级
    ui->label_showGradeUpCoefficient->setText(QString::number(value*2)+"%");
    game->setGradeUpCoefficient((float)ui->horizontalSlider->value()/100);

    if(0 == value) ui->label_showDifficult->setText("菜鸟");
    else if(20 > value)  ui->label_showDifficult->setText("萌新");
    else if(40 > value)  ui->label_showDifficult->setText("入门");
    else if(60 > value)  ui->label_showDifficult->setText("普通");
    else if(80 > value)  ui->label_showDifficult->setText("高手");
    else if(100 > value) ui->label_showDifficult->setText("巨佬");
    else
    {
        ui->label_showDifficult->setText("这也能卷？");//当200%,触发事件
        switch(message_count[MESSAGE_ROLL])//根据玩家有没有卷给出交互
        {
        case 0:
            QMessageBox::information(NULL,"2048","请不要卷了");
            message_count[MESSAGE_ROLL]++;
            break;
        case 1:
            QMessageBox::information(NULL,"2048","还卷是吧？");
            message_count[MESSAGE_ROLL]++;
            break;
        case 2:
            QMessageBox::information(NULL,"2048","球球你\n不 要 卷 啦555\n再卷人要没啦");
            message_count[MESSAGE_ROLL]++;
            break;
        default:
            QMessageBox::information(NULL,"2048","作者不幸被卷身亡");
            this->setWindowTitle("作者已故");//贴心的窗体标题变化
            break;
        }
    }
}

void MainWindow::on_pushButton_show_clicked()
{
    showRule();//显示教程的函数
}

void MainWindow::on_pushButton_clear_clicked()
{
    if(game->getGameStart())//作弊函数,入口开关很重要,不然又一大堆bug
    {
        game->clear();
        blinking = false;//取消闪烁也很重要,不然莫名其妙会闪
        showBroad();
        blinking = true;
    }
}

void MainWindow::on_pushButton_cheat_clicked()
{

    if(game->getGameStart())
    {
        game->cheat();
        blinking = false;
        showBroad();
        blinking = true;
    }
}

void MainWindow::on_pushButton_AI_clicked()
{
    AIrun = !AIrun;//开关状态切换
    if(AIrun)
    {
        sleepTime = 0;//加快速度,一开始没取消闪烁,会被闪烁待命卡慢,后来可能没有这个问题.不够我没试过
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
            srand(97*clock());//这里的优化产生了更加随机的数字,否则因为太快,同一个方向会连续很多次
            if (AI_step == rand()%4)
                AI_step = 3 - AI_step;
            else
            {
                AI_step = rand()%4;
            }

            switch(AI_step)
            {
            case 0:  game->process(CMD_UP);    break;
            case 1:  game->process(CMD_DOWN);  break;
            case 2:  game->process(CMD_LEFT);  break;
            case 3:  game->process(CMD_RIGHT); break;
            }
            showMessage();
            switch(game->judge())
            {
            case STAT_PROCESS:showBroad(); break;
            case STAT_WIN:
                showBroad();
                blinking = 0;
                QMessageBox::information(NULL,"2048","是不是极为先进");
                blinking = true;
                AIrun = false;
                sleepTime = 100;
                game->setGameStart(false);//结束游戏,并且调整状态
                break;
            case STAT_LOSE:
                game->clear();
                game->clear();
                game->setGameStart(true);//如果输了,就重设开始,并且清除两次
            }
            Sleep(15);//短暂停顿
        }
    }

    ui->pushButton_start->setEnabled(true);
    ui->pushButton_close->setEnabled(true);
    ui->pushButton_cheat->setEnabled(true);
    ui->pushButton_clear->setEnabled(true);
    ui->pushButton_change->setEnabled(true);
    sleepTime = 100;
}

void MainWindow::on_pushButton_change_clicked()//和子窗口的交互函数
{
    bigw = new BigWindow;
    bigw->show();
    this->hide();
    connect(bigw,SIGNAL(ExitWin()),this,SLOT(show()));
    QMessageBox::information(NULL,"2048","获胜条件变为4096\n\n");
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    if(ui->pushButton_start->isEnabled()&&game->getGameStart())//防止数字还没出完就开始,这样的话第二个数字生成会在操作停止以后
    {
        switch(event->key())//后来把wasd也加上了
        {
        case Qt::Key_Up: case Qt::Key_W:    game->process(CMD_UP);    break;
        case Qt::Key_Down: case Qt::Key_S:  game->process(CMD_DOWN);  break;
        case Qt::Key_Left: case Qt::Key_A:  game->process(CMD_LEFT);  break;
        case Qt::Key_Right: case Qt::Key_D: game->process(CMD_RIGHT); break;
        default: break;
        }
        showMessage();
        switch(game->judge())
        {
        case STAT_PROCESS:showBroad(); break;
        case STAT_WIN:
            showBroad();
            blinking = 0;
            if(game->getGameStart())
            {
                QMessageBox::information(NULL,"2048","以为这就赢了?");
                QMessageBox::information(NULL,"2048","好吧,确实");
                blinking = true;
                game->setGameStart(false);
            }
            break;
        case STAT_LOSE:
            showBroad();
            blinking = 0;
            QMessageBox::information(NULL,"2048","不会吧不会吧.不会这都有人赢不了吧"); break;
        }
    }
}

void MainWindow::showMessage()//刷新面板
{
    ui->label_showGrade->setText(QString::number(game->getGrade()));
    ui->label_showGradeBasic->setText(QString::number(game->getGradeBasic()));
    ui->label_showGradeUp->setText(QString::number(game->getGradeUp()));
    ui->label_showStep->setText(QString::number(game->getStep()));
    if(ui->horizontalSlider->value()==100&&!AIrun)
        switch(message_count[MESSAGE_ROLL])
        {
        case 0:
            QMessageBox::information(NULL,"2048","请不要卷了");
            message_count[MESSAGE_ROLL]++;
            break;
        case 1:
            QMessageBox::information(NULL,"2048","还卷是吧？");
            message_count[MESSAGE_ROLL]++;
            break;
        case 2:
            QMessageBox::information(NULL,"2048","球球你\n不 要 卷 啦555\n再卷人要没啦");
            message_count[MESSAGE_ROLL]++;
            break;
        case 3:
            QMessageBox::information(NULL,"2048","作者无了，你满意了吧");
            message_count[MESSAGE_ROLL]++;
            this->setWindowTitle("作者已故");
            break;
        default:break;
        };
}

void MainWindow::showBroad()
{
    //循环四行,每行刷新
    for(int i = 0;i < ROW;i++)
    {
        for(int j = 0;j < COL;j++)
        {
            if(game->getData(i,j)) findChild<QLabel *>("label_"+QString::number(i)+QString::number(j))->setText(QString::number(game->getData(i,j)));
            else                   findChild<QLabel *>("label_"+QString::number(i)+QString::number(j))->setText(" ");
            changeColor(findChild<QLabel *>("label_"+QString::number(i)+QString::number(j)), game->getData(i,j));
        }
    }
    if(game->getColour()!=-1&&game->getGameStart()&&blinking&&!game->getFull())//闪烁部分,这些条件缺一不可,否则会乱闪
    {
        blinking = false;
        Sleep(sleepTime);
        changeColorSlide(findChild<QLabel *>("label_"+QString::number(game->getColour()/4)+QString::number(game->getColour()%4)));
        Sleep(sleepTime);
        changeColor(findChild<QLabel *>("label_"+QString::number(game->getColour()/4)+QString::number(game->getColour()%4)), game->getData(game->getColour()/4,game->getColour()%4));
        blinking = true;
        Sleep(sleepTime);
        changeColorSlide(findChild<QLabel *>("label_"+QString::number(game->getColour()/4)+QString::number(game->getColour()%4)));
        Sleep(sleepTime);
        changeColor(findChild<QLabel *>("label_"+QString::number(game->getColour()/4)+QString::number(game->getColour()%4)), game->getData(game->getColour()/4,game->getColour()%4));
    }
}

//设置样式
void MainWindow::changeColor(QLabel* label, int num)
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

//闪烁函数
void MainWindow::changeColorSlide(QLabel* label)
{
    label->setStyleSheet("background-color: rgb(255,0,0);""font:bold 75 30pt ""微软雅黑""");
}

//待命函数
void MainWindow::Sleep(int msec)
{
    QTime dieTime = QTime::currentTime().addMSecs(msec);
    while( QTime::currentTime() < dieTime )
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
}

//规则显示函数
void MainWindow::showRule()
{
    QMessageBox::information(NULL,"2048","现在告知游戏规则：\n\n");
    QMessageBox::information(NULL,"2048","2048游戏：\n用方向键控制，\n合并数字，到达2048，");
    QMessageBox::information(NULL,"2048","右边显示了你的得分，\n等于合并过的数字之和\n加上产生数字乘以加成比例");
    QMessageBox::information(NULL,"2048","难度和数字产生概率相关,\n越高的等级产生的数字越随机\n");
    QMessageBox::information(NULL,"2048","你也许从未到达过2048,\n所以我赐予你神的力量:\n");
    QMessageBox::information(NULL,"2048","使用星辰之力,\n将所有2的最低次项化为星削\n");
    QMessageBox::information(NULL,"2048","你还可以使用            \n极     为    先    进\n的AI托管功能          ");
    QMessageBox::information(NULL,"2048","如果你忘记了我说的,\n点击右下角的查看教程\n欢迎随时回来");
    QMessageBox::information(NULL,"2048","现在,开始吧\n一旦开始,\n就请不要轻易放弃       ");
}
