import pickle
 
def init_user():
    # 先构造一个空字典，存储用户信息的文件 user.pkl
    user_dict = {}
    with open('user.pkl','wb') as f:
        pickle.dump(user_dict,f)
    print('初始化用户信息！！！')
    return None
 
if __name__ == '__main__':
    init_user()