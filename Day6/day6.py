dic = {
    
    '浙江':{
        '杭州':{
            '下沙':{
                '这':[], 
                '是':[],
            },
            '西湖':{
                '测':[],
                '试':[]
            },
            '临安':{'程':[]},
        },
        '绍兴':{
            '绍兴县':['序'],
            '嵊州':['所'],
        },
        '金华':[],
    },
    
    '北京':{
        '海淀':{
            '五道口':{'比':[]},
            '中关村':{'较':[]},
        },
        '朝阳':[],
        '东城':[],
    },
        
    '上海':{
        '闵行':{
            "人民广场":{'简':[]},
        },
        '闸北':{
            '火车战':{'陋':[]},
        },
        '浦东':{'的':[]},
    },
    '内蒙古':[],
    '陕西':[],
}


if __name__ == '__main__':
    current_layer = dic
    parent_layer = []
    flags = False
    tag = True
    i = 1
    while not flags:
        if tag:
            for key in current_layer:
                print(key)

        choose = input("请选择，输入b返回上一级菜单，输入q退出菜单:").strip()
        if choose in current_layer:
            parent_layer.append(current_layer)   #将当前的状态放入列表中
            if isinstance(current_layer[choose], list):
                print('已到达最后一层，请返回上一层')
                tag = False
            else:
                current_layer = current_layer[choose]
        elif choose == 'b':
            if tag == False:
                tag = True
            if parent_layer:
                current_layer = parent_layer.pop()
        elif choose == 'q':
            flags = True
        else:
            print("输入有误，请重新输入")
