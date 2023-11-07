import os           # 파일 수정한 시간 가져오기, 폴더 생성
import shutil       # 파일 복사(copy2 이용하면 메타정보 복사)
import copy         # 변수 깊은 복사
import glob         # 하위 폴더 내 모든 파일 리스트 작성
import natsort      # 하위 폴더 내 모든 파일 리스트 작성

# 하위 폴더 내 모든 파일 리스트 작성
def get_file_path(path):
    path += "\\**\\*?.*"        # *?.* 인 이유는 *.*으로 하면 ".숨김폴더가 포함됨" -> 폴더는 제외, 파일만 포함하기 위해 ? 추가
    temp_list = []
    for file in natsort.natsorted(glob.glob(path, recursive=True, include_hidden=True)):
        temp_list.append(file)
    return temp_list

def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    
    
    
# 각 저장매체별 sync폴더 목록
file_list = ["Gdrive", "nMybox", "외장하드", "Ddrive"]  # iCloud는 copy2가 안됨(수정한시간 바뀜)
file_list = []
file_time_list = []
each_drive_time = []
drive_list = ["G:\\내 드라이브\\Sync", "N:\\개인\\Sync", "E:\\Sync", "D:\\Sync"] # iCloud "C:\\Users\\iroo2\\iCloudDrive\\Sync"
# drive_list = ["D:\\Sync", "G:\\내 드라이브\\Sync", "N:\\개인\\Sync", "E:\\Sync", "C:\\Users\\iroo2\\iCloudDrive\\Sync"]
# drive_list = ["D:\\Sync_backup", "D:\\Sync"]
temp = ""
drive_path = ""
each_drive = []
each_drive_time = ""
file_time = ""
file_rel_path_set = set()
file_rel_path = []
drive_list_len = []
drive = ""
each_drive_abs = ""
each_drive_rel = ""
index = 0
file_name = ""
file_name_dict = dict()
temp_list = []
abs_path = ""
rel_path = ""
current_path_time = 0
temp_name = ""
drive_name = ""
which_drive = 0
recent_abs_path = []
recent_rel_path = []


# 위의 file_list 순서대로, 각 드라이브별 파일 목록이 이중 list로 저장됨
for drive_path in drive_list:
    try:
        temp = get_file_path(drive_path)
        file_list.append(temp)
    except:
        drive_list.remove(drive_path)
        print(drive_path, "에 연결할 수 없습니다.")
    

# 파일경로&명이 같으면 수정시간이 큰 경로를 저장하기
# dict (path : 시간1, 시간2, 시간3, 시간4)
# 초기에 dict를 만들어두고, 시간1234는 0,0,0,0으로 설정
# for 돌릴때마다 dict(path)의 해당 위치에 int 더하기

## 상대경로 set 만들기
for drive in drive_list:
    temp_list.append(0)     #dict 만들 때, [0,0,0,0]로 초기화하기 위함
    drive_list_len.append(len(drive))

for each_drive in file_list:
    for each_drive_abs in each_drive:
        each_drive_rel = each_drive_abs[drive_list_len[index]:]     # sync폴더의 root경로를 제외하고 저장
        file_rel_path.append(each_drive_rel)
    index += 1
file_rel_path_set=set(file_rel_path)
file_rel_path_set = list(file_rel_path_set)

## set에서 dict 만들기
for file_name in file_rel_path_set:
    file_name_dict[file_name] = temp_list

## 파일 수정한 시간 가져오고, dict의 각 위치에 추가
for i in range(len(drive_list)):
    for file_name in file_rel_path_set:
        try:
            file_time = int(os.path.getmtime(drive_list[i]+file_name))
            temp_list = copy.deepcopy(file_name_dict[file_name])
            temp_list[i] = copy.deepcopy(file_time)
            if file_time != 0 and i > 1:
                print(str(i)+"번", file_time)
            file_name_dict[file_name] = copy.deepcopy(temp_list)
        except:
            make_path_list = (drive_list[i]+file_name).split("\\")
            make_path_list.pop()
            make_path ="\\".join(make_path_list)
            try:
                os.makedirs(make_path)
            except:
                print("",end="")
            continue

# with open("dict.txt", "w") as dicttxt:
#     for i, j in file_name_dict.items():
#         dicttxt.write(str(i)+"\n"+str(j)+"\n\n")

# 시간이 큰 절대경로를 리스트에 저장
for file_name in file_rel_path_set:
    temp_list = file_name_dict[file_name]
    which_drive = temp_list.index(max(temp_list))
    recent_rel_path.append(file_name)
    recent_abs_path.append(drive_list[which_drive] + file_name)

# with open("abs.txt", "w") as abstxt:
#     for i in recent_abs_path:
#         abstxt.write(i+"\n")

# 절대경로의 리스트를 모든 경로로 복사, 덮어쓰기
for i in range(len(recent_rel_path)):
    clear()
    print(f'{int(i/len(recent_rel_path)*100)}% 완료')
    rel_path = recent_rel_path[i]
    abs_path = recent_abs_path[i]
    for drive in drive_list:
        paste_path = drive + rel_path
        if paste_path != abs_path:
            try:
                if abs(os.path.getmtime(abs_path) - os.path.getmtime(paste_path)) < 3:
                    continue
                else:
                    try:        #아래아래 except와 같음
                        paste_path_list = (paste_path).split("\\")
                        paste_path_list.pop()
                        paste_path ="\\".join(paste_path_list)
                        shutil.copy2(abs_path, paste_path)
                    except:
                        print(paste_path, abs_path)
            except:
                try:
                    paste_path_list = (paste_path).split("\\")
                    paste_path_list.pop()
                    paste_path ="\\".join(paste_path_list)
                    shutil.copy2(abs_path, paste_path)
                except:
                    print(paste_path, abs_path)

print("Sync Complete")