'''
简易王者荣耀
1. 设计王者荣耀中的英雄类,每个英雄对象可以对其他英雄对象使用技能
2. 英雄具备以下属性英雄名称,等级,血量和Q_hurt,W_hurt,E_hurt 三个伤害属性,表示各技能的伤害量
3. 具备以下技能Q W E三个技能都需要一个敌方英雄作为参数,当敌方血量小于等于0时输出角色死亡
'''

class hero:
    def __init__(self, name, level, blood, Q_hurt, W_hurt, E_hurt):
        self.name = name
        self.level = level
        self.blood = blood
        self.Q_hurt = Q_hurt
        self.W_hurt = W_hurt
        self.E_hurt = E_hurt
    
    def get_name(self):
        return self.name
    
    def get_blood(self):
        return self.blood
    
    def attack(self, enemy):
        global tag
        if enemy.blood > 0:
            print('英雄[%s]'%(self.name),end='')
            skill = input('选择技能（Q,W,E）：')
            if skill == 'Q'or skill == 'q':
                enemy.blood -= self.Q_hurt
                print('英雄[%s]使用[%s]技能攻击了英雄[%s]\n'
                      '英雄[%s]剩血量[%s]' % (self.name, skill, enemy.name, enemy.name, enemy.blood))

            elif skill == 'W' or skill == 'w':
                enemy.blood -= self.W_hurt
                print('英雄[%s]使用[%s]技能攻击了英雄[%s]\n'
                      '英雄[%s]剩血量[%s]' % (self.name, skill, enemy.name, enemy.name, enemy.blood))

            elif skill == 'E' or skill == 'e':
                enemy.blood -= self.E_hurt
                print('英雄[%s]使用[%s]技能攻击了英雄[%s]\n'
                      '英雄[%s]剩血量[%s]' % (self.name, skill, enemy.name, enemy.name, enemy.blood))
            else:
                print('请输入正确技能')


h1 = hero('盖伦',1,200,40,55,100)
h2 = hero('诺手',1,220,50,46,90)

while True:
    h1.attack(h2)
    b = h2.get_blood()
    if b<=0:
        print('英雄[%s]死亡' % h2.get_name() )
        break
    
    h2.attack(h1)
    a = h1.get_blood()
    if a<=0:
        print('英雄[%s]死亡' % h1.get_name() )
        break
    