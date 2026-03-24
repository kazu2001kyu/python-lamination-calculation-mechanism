import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import csv
import numpy as np
from scipy.optimize import minimize
import matplotlib as mpl
from decimal import Decimal, ROUND_HALF_UP
import colorsys
import matplotlib.patches as patches
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap

mpl.rcParams['font.family'] = 'MS Gothic'  # WindowsならMSゴシックが無難

mpl.rcParams.update({
    'font.size': 14,             # 全体のフォントサイズ
    'axes.titlesize': 18,        # タイトルサイズ
    'axes.labelsize': 16,        # 軸ラベル
    'xtick.labelsize': 14,       # x軸目盛り
    'ytick.labelsize': 14,       # y軸目盛り
    'legend.fontsize': 14,       # 凡例フォント
    'lines.linewidth': 2.5,      # 線の太さ
    'figure.dpi': 100,           # 解像度
})

# 計算のステップ間隔
step = 5

# 三刺激値におけるK定数(宣言)
K=0

# R"G"B"計算時に使用する，sRGB変換マトリクス．
tosRGB = [
        [3.2406, -1.5372, -0.4986],
        [-0.9689, 1.8758, 0.0415],
        [0.0557, -0.2040, 1.0570]
    ]

## dataファイル(光路差100付近:基準)におけるファイルpass/2024.1.16^F 光路差の精密測定(Excel)より算出/**より精確なdata必要
file_name = "python-lamination-calculation-mechanism-main/data/data_d_100.csv"
# dataファイル(光源:白色LED光源)におけるファイルpass
file_name_light = "python-lamination-calculation-mechanism-main/data/data_light_iphone13mini.csv"
# dataファイル(補正データ:C2)におけるファイルpass
file_name_correct = "python-lamination-calculation-mechanism-main/data/R.csv"
# dataファイル(等色関数 row[１]=x(λ),row[2]=y(λ),rao[3]=z(λ))におけるファイルpass
file_name_color_f = "python-lamination-calculation-mechanism-main/data/data_e_color.csv"


# 光路差(with open関数による，基準(100nm 付近)の光路差のinstal
with open(file_name, encoding='utf8') as f1:
    reader = csv.reader(f1)
    header = next(reader)

    λ = 380
    dd = []
    λλ = []
    for row in reader:
        λ = int(row[0])
        d = float(row[1])
        dd.append(d)
        λλ.append(λ)
        
        if int(row[0]) != λ:
            λ += 1
            # 繰り返し施行するための，配列のリセット
            if λ > 750:
                break               


#偏光状態の記述のために，installしたfiledataの型をlistからarrayへ変更
array_dd = np.array(dd)
array_λλ = np.array(λλ)


# 光源(with open関数による，白色LED光源のdataのinstall)
with open(file_name_light, encoding='utf8') as f2:
    reader = csv.reader(f2)
    header = next(reader)

    λ = 380
    ll = []
    λλ = []
    for row in reader:
        λ = int(row[0])
        l = float(row[1])
        ll.append(l)
        
        if int(row[0]) != λ:
            λ += 1
            # 繰り返し施行するための，配列のリセット
            if λ > 750:
                break           

#偏光状態の記述のために，installしたfiledataの型をlistからarrayへ変更
array_ll = np.array(ll)   
#正規化のために, スペクトルAの最大値を検出
max_spcll = max(array_ll)
#正規化したスペクトルAの算出
NspcA = [num/max_spcll  for num in array_ll]


# 光源(with open関数による，補正dataのinstall)
with open(file_name_correct, encoding='utf8') as f3:
    reader = csv.reader(f3)
    header = next(reader)

    λ = 380
    cc = []
    λλ = []
    for row in reader:
        λ = int(row[0])
        c = float(row[1])
        cc.append(c)
        
        if int(row[0]) != λ:
            λ += 1
            # 繰り返し施行するための，配列のリセット
            if λ > 750:
                break 
    

#偏光状態の記述のために，installしたfiledataの型をlistからarrayへ変更
array_cc = np.array(cc)
#正規化のために, スペクトルAの最大値を検出
max_spccc = max(array_cc)
#正規化したスペクトルAの算出
Nspcc = [num/max_spcll  for num in array_cc]
#光源*補正データの正規化データへ
sp = np.array(Nspcc)*np.array(NspcA)
max_sp = max(sp)
spN = [num/max_sp for num in sp]

# 光源(with open関数による，等色関数のinstall)
with open(file_name_color_f, encoding='utf8') as f4:
    reader = csv.reader(f4)
    header = next(reader)

    λ = 380
    cfx = []
    cfy = []
    cfz = []
    λλ = []
    for row in reader:
        λ = int(row[0])
        fx = float(row[1])
        fy = float(row[2])
        fz = float(row[3])
        cfx.append(fx)
        cfy.append(fy)
        cfz.append(fz)
        
        if int(row[0]) != λ:
            λ += 1
            # 繰り返し施行するための，配列のリセット
            if λ > 750:
                break 

cfx.append(fx)
cfy.append(fy)
cfz.append(fz)

#偏光状態の記述のために，installしたfiledataの型をlistからarrayへ変更
array_cfx = np.array(cfx)
array_cfy = np.array(cfy)
array_cfz = np.array(cfz)
#正規化のために, 各等色関数の最大値を検出
max_cfx = max(array_cfx)
max_cfy = max(array_cfy)
max_cfz = max(array_cfz)
#正規化した各等色関数の算出
Nspcfx = [num/max_cfx  for num in array_cfx]
Nspcfy = [num/max_cfy  for num in array_cfy]
Nspcfz = [num/max_cfz  for num in array_cfz]


#[k定数について]___________________________________________________________________________________________
for i in range(380,751): #各λにおける値の算出
        K += float((array_ll[i-380]*array_cfy[i-380]))
K = 1.0/ K # 光源の際の値を基準として,Y=1とする


# ガウス関数
def gauss(x, A, mu, sigma):
    return A * np.exp(-((x - mu) ** 2) / (2 * (sigma/2.356) ** 2))

x = np.linspace(380, 750, 371)

# スペクトル更新
def update_plot(_=None):
    x = np.linspace(380, 750, 371)
    y_total = np.zeros_like(x)

    ax1.clear()
    ax2.clear()

    colors = ['red', 'green', 'blue', 'purple']
    for i in range(4):
        A, mu, sigma = params[i]
        y = gauss(x, A, mu, sigma)
        y_total += y
        ax1.plot(x, y, '--', label=f'Gauss {i+1}', color=colors[i])
    
    ax1.plot(x, y_total, color='black', linewidth=2, label='ガウス関数(合成)')
    ax1.legend()
    ax1.set_title("4 Gaussian Functions + Sum")
    ax1.set_xlabel("Wavelenght [nm]")
    ax1.set_ylabel("Intensity [arb.units]")
    ax1.grid(True)

    
    # 右側スペクトル
    max_ll = max(array_ll)
    #正規化したスペクトルAの算出
    N_ll = [num/max_ll for num in array_ll]
    array_y_total = np.array(y_total)
    max_gauss=max(y_total)
    #正規化したスペクトルAの算出
    N_gauss = [num/max_gauss for num in array_y_total]
    # リストをnumpy配列に変換して要素ごとの掛け算
    N_gauss = np.array(N_gauss) 
    N_ll = np.array(N_ll)
    N_spectrum_gauss = N_gauss*N_ll
    max_Ns = max(N_spectrum_gauss)
    In = Intensity_slider.get()
    #正規化したスペクトルAの算出
    N_g = [num/max_Ns*In for num in N_spectrum_gauss]
    ax2.plot(x, N_g, color='black', linewidth=2,label="ガウス関数(合成-正規化)")
    #光源の正規化スペクトル
    ax2.plot(x,spN,color="blue",linewidth=2,label="光源")
    ax2.set_title("N_gauss*spectrum")
    ax2.set_xlabel("Wavelength [nm]")
    ax2.set_ylabel("Intensity [arb.units]")
    ax2.grid(True)
    ax2.legend()
    canvas.draw()
    
def y_totalnum():
    y_total = np.zeros_like(x)
    for i in range(4):
        A, mu, sigma = params[i]
        y = gauss(x, A, mu, sigma)
        y_total += y
        # 右側スペクトル
    max_ll = max(array_ll)
    #正規化したスペクトルAの算出
    N_ll = [num/max_ll for num in array_ll]
    array_y_total = np.array(y_total)
    max_gauss=max(y_total)
    #正規化したスペクトルAの算出
    N_gauss = [num/max_gauss for num in array_y_total]
    # リストをnumpy配列に変換して要素ごとの掛け算
    N_gauss = np.array(N_gauss) 
    N_ll = np.array(N_ll)
    N_spectrum_gauss = N_gauss*N_ll
    max_Ns = max(N_spectrum_gauss)
    In = Intensity_slider.get()
    #正規化したスペクトルAの算出
    N_g = [num/max_Ns*In for num in N_spectrum_gauss]
    return N_g

# スライダー変更処理
def slider_changed(_=None):
    i = current_gauss[0]
    params[i][0] = amp_slider.get()
    params[i][1] = mu_slider.get()
    params[i][2] = sigma_slider.get()
    update_plot()

# Gauss関数選択
def select_gauss(index):
    current_gauss[0] = index
    amp_slider.set(params[index][0])
    mu_slider.set(params[index][1])
    sigma_slider.set(params[index][2])
    current_label.config(text=f"調整中: Gauss {index+1}")

# fittingの実行
def fitting():
    x = np.linspace(380, 750, 371)  # A と B のデータ数を統一
    def r_theta(theta):  # 回転行列R(θ）
        return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    def mai_r_theta(theta):  # 回転行列R(-θ）
        return np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])

    def jhons(theta):  # ジョーンズマトリクス
        return np.array([[np.sin(theta)**2, -np.sin(theta)*np.cos(theta)], [-np.sin(theta)*np.cos(theta), np.cos(theta)**2]])

    
    #多変数関数のスペクトルB1
    def spectrum_B1(params, x):
        a1, a2, a3 ,a4,a5,a6,a7,a8,a9,a10 = params
        a2 = round(a2)
        a3 = round(a3)
        a4 = round(a4)
        
        spcA = []
        #光路差(各変動-配列値)
        array_ddc1 = [num*(a8/100) for num in np.array(dd)]
        array_ddc2 = [num*(a9/100) for num in np.array(dd)]
        array_ddc3 = [num*(a10/100) for num in np.array(dd)]
        # 偏光板一枚目の回転角
        a = np.deg2rad(-a7)
        E_1 = np.array([[-np.sin(a)], [np.cos(a)]])
        # セロハン二枚目の回転角
        b = np.deg2rad(a6-a7)
        # セロハン三枚目の回転角
        e = np.deg2rad(a5-a7)
        # 偏光板二枚目の回転角
        if a1 == 1: # 直交ニコル配置ver
            c = np.deg2rad(-a7-90)
        elif a1 ==2: # 平行ニコル配置ver
            c = np.deg2rad(-a7)
        elif a1 == 3: # 45°配置ver
            c = np.deg2rad(-a7-45)

        for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
            # 波長
            l = i
            ## 位相差(手前x枚)
            delta = 2*array_ddc1[l-380]*np.pi/l
            ## 位相差(中p枚)
            deltap = 2*array_ddc2[l-380]*np.pi/l
            ## 位相差(奥z枚)
            deltaz = 2*array_ddc3[l-380]*np.pi/l
            # セロハンの項(1jで虚数iを明示的に表現):x枚
            cellox = np.array([[1, 0], [0, np.exp(-1j*delta*a4)]])
            # セロハンの項(1jで虚数iを明示的に表現):p枚
            cellop = np.array([[1, 0], [0, np.exp(-1j*deltap*a3)]])
            # セロハンの項(1jで虚数iを明示的に表現):z枚
            celloz = np.array([[1, 0], [0, np.exp(-1j*deltaz*a2)]])
            # E_2への変換
            E_2 = np.dot(cellox, E_1)
            # E_3への変換
            E_3 = np.dot(r_theta(b), np.dot(
                cellop, np.dot(mai_r_theta(b), E_2)))
            #E_4への変換
            E_4 = np.dot(r_theta(e), np.dot(
                celloz, np.dot(mai_r_theta(e), E_3)))
            # E_5への変換
            E_5 = np.dot(jhons(c), E_4)
            # 各波長でのI(光強度)を算出する
            I = (np.abs(np.abs(E_5[0]**2) + np.abs(E_5[1]**2)))
            #2.強度配列に光源データ配列を積した測定直交スペクトルを算出　
            #3.補正データを積した補正測定直交配置スペクトルを算出
            spc = I*(spN[l-380])
            #spcλ = float(spc)
            spcλ = spc.item()
            spcA.append(spcλ)
        
        #用意したスペクトルdataの型をlistからarrayへ変更
        array_spcA = np.array(spcA)
        # グラフ描画と最適化の為の変数用意
        x = np.linspace(380, 750, 371)  # A と B のデータ数を統一
        AA = array_spcA
        return AA
    
    # 目的関数（最小化する二乗誤差）
    def objective(params):
        A = np.array(y_totalnum())  # numpy 配列に変換
        B = np.array(spectrum_B1(params, x))  # numpy 配列に変換
        return np.sum(( A - B) ** 2)  # A と B の差の二乗和
    
    # 初期値 (nn,zz,pp,xx,ε,β,w)
    initial_guess = [2.0, 2.0, 1.0, 2.0, 45, 30, 10, 300,300,300]
    
    # 現在の制約モードを判定
    mode = constraint_mode_var.get()
    if mode == "common":# 共通制約時
        val_low = common_lower_var.get()
        val_up = common_upper_var.get()
        try:
            od1_lower = float(val_low)
            od1_upper = float(val_up)
            od2_lower = float(val_low)
            od2_upper = float(val_up)
            od3_lower = float(val_low)
            od3_upper = float(val_up)
        except ValueError:
            od1_lower = 200
            od1_upper = 400
            od2_lower = 200
            od2_upper = 400
            od3_lower = 200
            od3_upper = 400
        
    elif mode == "individual":
        try:
            od1_lower = float(od1_lower_var.get())
            od1_upper = float(od1_upper_var.get())
            od2_lower = float(od2_lower_var.get())
            od2_upper = float(od2_upper_var.get())
            od3_lower = float(od3_lower_var.get())
            od3_upper = float(od3_upper_var.get())
        except ValueError:
            od1_lower = 200
            od1_upper = 400
            od2_lower = 200
            od2_upper = 400
            od3_lower = 200
            od3_upper = 400
            
    # 枚数に関する入力値の受け取り
    od1_th_lower = float(od1_thick_lower_var.get())
    od1_th_upper = float(od1_thick_upper_var.get())
    od2_th_lower = float(od2_thick_lower_var.get())
    od2_th_upper = float(od2_thick_upper_var.get())
    od3_th_lower = float(od3_thick_lower_var.get())
    od3_th_upper = float(od3_thick_upper_var.get())
    
    # 角度に関する入力値の受け取り
    od1_an_lower = float(od1_angle_lower_var.get())
    od1_an_upper = float(od1_angle_upper_var.get())
    od2_an_lower = float(od2_angle_lower_var.get())
    od2_an_upper = float(od2_angle_upper_var.get())
    od3_an_lower = float(od3_angle_lower_var.get())
    od3_an_upper = float(od3_angle_upper_var.get())
    
    mode = polarization_mode_var.get()
    if mode == "orthogonal":# 直交時
        P_plate =1
        
    elif mode == "parallel": #平行時
        P_plate=2

    bounds = [
        (P_plate, P_plate), (od3_th_lower, od3_th_upper), (od2_th_lower, od2_th_upper),
        (od1_th_lower, od1_th_upper), (od3_an_lower, od3_an_upper), (od2_an_lower, od2_an_upper),
        (od1_an_lower, od1_an_upper), (od1_lower, od1_upper),
        (od2_lower, od2_upper),(od3_lower, od3_upper)
    ]
    
    # 最適化の実行
    result = minimize(objective, initial_guess, method="SLSQP", bounds=bounds)

    # 最適解
    a1_opt, a2_opt, a3_opt, a4_opt, a5_opt, a6_opt, a7_opt, a8_opt, a9_opt, a10_opt = result.x
    print(f"最適解:\n"
        f"a1 = {a1_opt}, a2 = {a2_opt}, a3 = {a3_opt}\n"
        f"a4 = {a4_opt}, a5 = {a5_opt}, a6 = {a6_opt}\n"
        f"a7 = {a7_opt}, a8 = {a8_opt},a9 = {a9_opt},a10 = {a10_opt}")
    
    # 最適化されたスペクトル B1
    B1_opt = spectrum_B1([a1_opt, a2_opt, a3_opt, a4_opt, a5_opt, a6_opt, a7_opt, a8_opt,a9_opt, a10_opt], x)
    
    if a1_opt==1:
        B2_opt = spectrum_B1([2, a2_opt, a3_opt, a4_opt, a5_opt, a6_opt, a7_opt, a8_opt,a9_opt, a10_opt], x)
    elif a1_opt==2:
        B2_opt = spectrum_B1([1, a2_opt, a3_opt, a4_opt, a5_opt, a6_opt, a7_opt, a8_opt,a9_opt, a10_opt], x)
    
    
    #最適解によるRGB
    colornow = fitting_color([a1_opt, a2_opt, a3_opt, a4_opt, a5_opt, a6_opt, a7_opt, a8_opt,a9_opt, a10_opt])
    # 決定係数の算出
    def r_squared(A, B):
        # A: 観測データ（基準となるスペクトル, numpy配列）
        # B: 予測データ（最適化されたスペクトル, numpy配列）
        A = np.array(A)
        B = np.array(B)
        ss_res = np.sum((A - B) ** 2)  # 残差平方和
        ss_tot = np.sum((A - np.mean(A)) ** 2)  # 全変動
        return 1 - (ss_res / ss_tot)
    AAA = y_totalnum() #gaussの合成スペクトル
    gauss_RGB = gauss_color(AAA) #gaussの合成光が存在する場合の実際の色
    #★ RGBの補正. 強度に応じてRGBの比率を保ちながら値を変更する.その際にはスペクトルであるB1_optを使用 とHSV描画へ
    colorget = correctional_rgb(colornow,B1_opt,sp) #[arr_Rr,arr_Gr,arr_Br], 最適化スペクトル,正規化光源スペクトル(補正済み)
    gauss_HSV(gauss_RGB,AAA,sp) # gauss_RGBについて, 補正をしてHSV色表示をする
    
    R2 = r_squared(AAA, B1_opt) #step1 決定係数R^2
    #自由度調整済み決定係数の算出
    Rf2 = 1-(1-R2)*(370)/369
    Rf2_rounded = round(Rf2, 3)
    print("rgb-"+str(colornow))
    print("RGB-"+str(colorget))
    print("Rf2-"+str(Rf2_rounded))
    #毎回初期化
    ax2.clear()
    
    x = np.linspace(380, 750, 371)
    y_total = np.zeros_like(x)

    colors = ['red', 'green', 'blue', 'purple']
    for i in range(4):
        A, mu, sigma = params[i]
        y = gauss(x, A, mu, sigma)
        y_total += y
    
    # 右側スペクトル
    max_ll = max(array_ll)
    #正規化したスペクトルAの算出
    N_ll = [num/max_ll for num in array_ll]
    array_y_total = np.array(y_total)
    max_gauss=max(y_total)
    #正規化したスペクトルAの算出
    N_gauss = [num/max_gauss for num in array_y_total]
    # リストをnumpy配列に変換して要素ごとの掛け算
    N_gauss = np.array(N_gauss) 
    N_ll = np.array(N_ll)
    N_spectrum_gauss = N_gauss*N_ll
    max_Ns = max(N_spectrum_gauss)
    In = Intensity_slider.get()
    #正規化したスペクトルAの算出
    N_g = [num/max_Ns*In for num in N_spectrum_gauss]
    ax2.plot(x, N_g, color='black', linewidth=2,label="ガウス関数(合成-正規化)")
    #光源の正規化スペクトル
    ax2.plot(x,spN,color="blue",linewidth=2,label="光源")
    ax2.set_title("N_gauss*spectrum")
    ax2.set_xlabel("Wavelength [nm]")
    ax2.set_ylabel("Intensity [arb.units]")
    ax2.grid(True)
    ax2.legend()    
    
    if a1_opt==1:
        ax2.plot(x,B1_opt,color='red', linewidth=1.5, label='Fit_直交')  
        ax2.plot(x,B2_opt,color='green', linewidth=1.5, label='Fit_平行')  
        #ax2.plot(x,B1_opt+B2_opt,color='c', linewidth=0.5, label='Fitting Spectrum_sum')  
        ax2.legend()
    elif a1_opt==2:
        ax2.plot(x,B1_opt,color='green', linewidth=1.5, label='Fit_平行')  
        ax2.plot(x,B2_opt,color='red', linewidth=1.5, label='Fit_直交')  
        #ax2.plot(x,B1_opt+B2_opt,color='c', linewidth=1.5, label='Fitting Spectrum_sum')  
        ax2.legend()

    # 最適化結果の更新
    if a1_opt==1:
        opt_result_label.config(text=f"直交配置 : 手前-枚数={a4_opt:.0f}, 中-枚数={a3_opt:.0f}, 奥-枚数={a2_opt:.0f}, 手前-角度={a7_opt:.2f},中-角度={a6_opt:.2f},奥-角度={a5_opt:.2f},光路差⑴={a8_opt:.2f},光路差⑵={a9_opt:.2f},光路差⑶={a10_opt:.2f}", font=("Arial", 15))
    elif a1_opt==2:
        opt_result_label.config(text=f"平行配置 : 手前-枚数={a4_opt:.0f}, 中-枚数={a3_opt:.0f}, 奥-枚数={a2_opt:.0f}, 手前-角度={a7_opt:.2f},中-角度={a6_opt:.2f},奥-角度={a5_opt:.2f},光路差⑴={a8_opt:.2f},光路差⑵={a9_opt:.2f},光路差⑶={a10_opt:.2f}", font=("Arial", 15))
    
    # 再描画
    canvas.draw()
    y_total = sum(gauss(x, *p) for p in params)
    #area = np.trapz(y_total, x)
    hex_color = "#{:02x}{:02x}{:02x}".format(int(colorget[0]), int(colorget[1]), int(colorget[2]))
    color_box.config(bg=hex_color)
    result_label.config(text="R-"+str(int(colorget[0]))+"-G-"+str(int(colorget[1]))+"-B-"+str(int(colorget[2])),font=("Arial", 20)) # フォント名とサイズを指定)

def fittingGauss():
    AAA = y_totalnum() #gaussの合成スペクトル
    gauss_RGB = gauss_color(AAA) #gaussの合成光が存在する場合の実際の色
    #★ RGBの補正. 強度に応じてRGBの比率を保ちながら値を変更する.その際にはスペクトルであるB1_optを使用 とHSV描画へ
    gauss_HSV2(gauss_RGB,AAA,sp) # gauss_RGBについて, 補正をしてHSV色表示をする
    # 再描画
    canvas.draw()


def correctional_rgb(rgbnow,light_opt,light_s):
    sumR_opt = 0.0
    sumG_opt = 0.0
    sumB_opt = 0.0
    sumR_ls  = 0.0
    sumG_ls  = 0.0
    sumB_ls  = 0.0
    #RGBの受け取り
    r,g,b = rgbnow
    #辞書の作成
    d = {'R':r,'G':g,'B':b}
    #RGBのうちどれが最大化がどれかを参照(同値255,255,255の場合は最初の値..?)
    getlarge=max(d, key=d.get)  #
    getlargeRGB=max([r,g,b])
    if getlarge=='R':
        for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
            sumR_opt+=light_opt[i-380]*Nspcfx[i-380]
            sumR_ls+=light_s[i-380]*Nspcfx[i-380]
        ratio = (sumR_opt**(1/2.4))/(sumR_ls**(1/2.4))
        print("sumR_opt"+str(sumR_opt))
        print("sumR_ls"+str(sumR_ls))
    elif getlarge=='G':
        for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
            sumG_opt+=light_opt[i-380]*Nspcfy[i-380]
            sumG_ls+=light_s[i-380]*Nspcfy[i-380]
        ratio = (sumG_opt**(1/2.4))/(sumG_ls**(1/2.4))
        print("sumG_opt"+str(sumG_opt))
        print("sumG_ls"+str(sumG_ls))
    else :
        for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
            sumB_opt+=light_opt[i-380]*Nspcfz[i-380]
            sumB_ls+=light_s[i-380]*Nspcfz[i-380]
        ratio = (sumB_opt**(1/2.4))/(sumB_ls**(1/2.4))
        print("sumB_opt"+str(sumB_opt))
        print("sumB_ls"+str(sumB_ls))
    
    print("ratio-"+str(ratio))

    #ratioによるRGBの補正
    r*=ratio
    g*=ratio
    b*=ratio
    colorsrgb=[r, g, b]
    color = [(r/255, g/255, b/255)]
    # RGB値をHSV値に変換する．
    HSV = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    arr_H = HSV[0]
    arr_S = HSV[1]
    arr_V= HSV[2]
    #グラフの描画へ
    # グラフの描画へ（毎回リセット）これにより履歴を残さない
    ax3.clear()  
    ax3.grid(True)  # grid表示ON
    ax3.set_xlim(-1,1)
    ax3.set_ylim(-1,1)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    # π表記に変換（例：0.50π, 1.25πなど）
    theta_pi_str = f"{arr_H * 2:.2f}π"
    ax3.set_title(f"H-{theta_pi_str} - S-{arr_S:.2f} - V-{arr_V:.2f}", fontname="Arial", fontsize=20)  # グラフタイトル
    #グラフに円を描写する(ec = edge color)
    c = patches.Circle(xy=(0, 0), radius=1.0,fill=False, ec='r')
    img = plt.imread("python-lamination-calculation-mechanism-main/hsv_wheel_transparent.png")
    ax3.imshow(img, extent=[-1, 1, -1, 1], alpha=0.6, zorder=0)
    # グラフに円を追加する．
    ax3.add_patch(c)
    #位置の指定
    X = (arr_S)*np.cos(2*np.pi*(arr_H))
    Y = (arr_S)*np.sin(2*np.pi*(arr_H))
    ax3.scatter(X,Y,s=20,c="k",label="最適化関数_RGB")
    ax3.legend(loc="upper right", fontsize=10)  # 凡例を自動配置＆フォントサイズ指定
    
    # === Vスケーリングバーの追加 ===
    # 別のAxes（ax_vbar）をグラフ横に追加
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    # === スケールバー（明度 V 0〜1）追加 ===
    # === Vスケーリングバーの追加 ===
    divider = make_axes_locatable(ax3)
    ax_vbar = divider.append_axes("right", size="5%", pad=0.1)

    # ① グラデーション生成（arr_H, arr_S固定で、Vを0→1に変化させた後に上下逆転）
    v_vals = np.linspace(0, 1, 256)
    colors = [colorsys.hsv_to_rgb(arr_H, arr_S, v) for v in v_vals]
    cmap_custom = ListedColormap(colors)

    # === ① グラデーション表示（上下逆転）===
    v_gradient = v_vals[::-1].reshape(-1, 1)  # 
    ax_vbar.imshow(v_gradient, aspect='auto', cmap=cmap_custom)

    # y軸を右側に、上を1.00、下を0.00に
    ax_vbar.yaxis.tick_right()
    ax_vbar.yaxis.set_label_position("right")
    ax_vbar.set_title("V", fontsize=12)    
    # === 目盛り（上:1.00〜下:0.00）を 0.1刻みで表示 ===
    # === y軸の目盛り（0.1刻み）を設定：上が1.00、下が0.00 ===
    v_tick_values = np.arange(1.0, -0.01, -0.1)  # [1.0, 0.9, ..., 0.0]
    yticks = [int((1.0 - v) * 255) for v in v_tick_values]  # V=1.0 → 0（上）, V=0.0 → 255（下）
    yticklabels = [f"{v:.2f}" for v in v_tick_values]
    ax_vbar.set_yticks(yticks)
    ax_vbar.set_yticklabels(yticklabels)
    
    # ② 現在のV位置のインデックス（逆順に合わせて変更）
    #v_index = int(arr_V * 255)  # ← 変更前：(1 - arr_V) * 255
    v_index = int((1 - arr_V) * 255)  # 
    # ② 補色の計算（RGB→補色RGB）
    r, g, b = colorsys.hsv_to_rgb(arr_H, arr_S, arr_V)
    comp_color = (1 - r, 1 - g, 1 - b)  # 補色（RGBの反転）

    # ② 水平線の描画（補色で表示）
    ax_vbar.axhline(v_index, color=comp_color, linewidth=5)

    # x軸目盛りは非表示
    ax_vbar.set_xticks([])
        
    print(f"最適解:\n"
        f"R = {r}, G = {g}, B = {b}\n"
        f"H = {arr_H}, S = {arr_S}, V = {arr_V}\n"
        f"X = {X}, Y = {Y}")
    return colorsrgb

# gauss_RGBの補正を行い, HSV色表示をする関数
def gauss_HSV(rgbgauss,light_opt,light_s):
    sumR_opt = 0.0
    sumG_opt = 0.0
    sumB_opt = 0.0
    sumR_ls  = 0.0
    sumG_ls  = 0.0
    sumB_ls  = 0.0
    #RGBの受け取り
    r,g,b = rgbgauss
    
    #混色比を使用せず、三刺激値から色を算出する仕様への変更により、以下の強度補正は不要。
    #辞書の作成
    #d = {'R':r,'G':g,'B':b}
    #RGBのうちどれが最大化がどれかを参照(同値255,255,255の場合は最初の値..?)
    #getlarge=max(d, key=d.get)  #
    
    #if getlarge=='R':
        #for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
        #   sumR_opt+=light_opt[i-380]*Nspcfx[i-380]
        #  sumR_ls+=light_s[i-380]*Nspcfx[i-380]
        #ratio = (sumR_opt)/(sumR_ls)
        #print("GsumR_opt"+str(sumR_opt))
        #print("GsumR_ls"+str(sumR_ls))
    #elif getlarge=='G':
        #for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
        #    sumG_opt+=light_opt[i-380]*Nspcfy[i-380]
        #    sumG_ls+=light_s[i-380]*Nspcfy[i-380]
        #ratio = (sumG_opt)/(sumG_ls)
        #print("GsumG_opt"+str(sumG_opt))
        #print("GsumG_ls"+str(sumG_ls))
    #else :
        #for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
        #    sumB_opt+=light_opt[i-380]*Nspcfz[i-380]
        #    sumB_ls+=light_s[i-380]*Nspcfz[i-380]
        #ratio = (sumB_opt)/(sumB_ls)
        #print("GsumB_opt"+str(sumB_opt))
        #print("GsumB_ls"+str(sumB_ls))
    
    #print("Gratio-"+str(ratio))

    #ratioによるRGBの補正
    #r*=ratio
    #g*=ratio
    #b*=ratio
    # RGB値をHSV値に変換する．
    HSV = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    arr_H = HSV[0]
    arr_S = HSV[1]
    arr_V= HSV[2]
    #グラフの描画へ
    #位置の指定
    X = (arr_S)*np.cos(2*np.pi*(arr_H))
    Y = (arr_S)*np.sin(2*np.pi*(arr_H))
    ax3.scatter(X,Y,s=30, marker='x', c='r', linewidths=1.5, label="Gauss関数_RGB")
    ax3.legend(loc="upper right", fontsize=10)  # 凡例を自動配置＆フォントサイズ指定

def gauss_HSV2(rgbgauss,light_opt,light_s):
    sumR_opt = 0.0
    sumG_opt = 0.0
    sumB_opt = 0.0
    sumR_ls  = 0.0
    sumG_ls  = 0.0
    sumB_ls  = 0.0
    #RGBの受け取り
    r,g,b = rgbgauss
    
    #混色比を使用せず、三刺激値から色を算出する仕様への変更により、以下の強度補正は不要。
    #辞書の作成
    #d = {'R':r,'G':g,'B':b}
    #RGBのうちどれが最大化がどれかを参照(同値255,255,255の場合は最初の値..?)
    #getlarge=max(d, key=d.get)  #
    
    #if getlarge=='R':
    #    for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
    #        sumR_opt+=light_opt[i-380]*Nspcfx[i-380]
    #        sumR_ls+=light_s[i-380]*Nspcfx[i-380]
    #    ratio = ((sumR_opt)/(sumR_ls))**(1/2.4)
    #    print("GsumR_opt"+str(sumR_opt))
    #    print("GsumR_ls"+str(sumR_ls))
    #elif getlarge=='G':
    #    for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
    #        sumG_opt+=light_opt[i-380]*Nspcfy[i-380]
    #        sumG_ls+=light_s[i-380]*Nspcfy[i-380]
    #    ratio = ((sumG_opt)/(sumG_ls))**(1/2.4)
    #    print("GsumG_opt"+str(sumG_opt))
    #    print("GsumG_ls"+str(sumG_ls))
    #else :
    #    for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
    #        sumB_opt+=light_opt[i-380]*Nspcfz[i-380]
    #        sumB_ls+=light_s[i-380]*Nspcfz[i-380]
    #    ratio = ((sumB_opt)/(sumB_ls))**(1/2.4)
    #    print("GsumB_opt"+str(sumB_opt))
    #    print("GsumB_ls"+str(sumB_ls))
    
    #print("Gratio-"+str(ratio))

    #ratioによるRGBの補正
    #r*=ratio
    #g*=ratio
    #b*=ratio
    # RGB値をHSV値に変換する．
# RGB値をHSV値に変換する．
    HSV = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    arr_H = HSV[0]
    arr_S = HSV[1]
    arr_V= HSV[2]
    #グラフの描画へ
    # グラフの描画へ（毎回リセット）これにより履歴を残さない
    ax3.clear()  # ← これを追加！
    ax3.grid(True)  # grid表示ON
    ax3.set_xlim(-1,1)
    ax3.set_ylim(-1,1)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    # π表記に変換（例：0.50π, 1.25πなど）
    theta_pi_str = f"{arr_H * 2:.2f}π"
    ax3.set_title(f"H-{theta_pi_str} - S-{arr_S:.2f} - V-{arr_V:.2f}", fontname="Arial", fontsize=20)  # グラフタイトル
    #グラフに円を描写する(ec = edge color)
    c = patches.Circle(xy=(0, 0), radius=1.0,fill=False, ec='r')
    img = plt.imread("python-lamination-calculation-mechanism-main/hsv_wheel_transparent.png")
    ax3.imshow(img, extent=[-1, 1, -1, 1], alpha=0.6, zorder=0)
    # グラフに円を追加する．
    ax3.add_patch(c)
    #位置の指定
    X = (arr_S)*np.cos(2*np.pi*(arr_H))
    Y = (arr_S)*np.sin(2*np.pi*(arr_H))
    ax3.scatter(X,Y,s=20,c="k",label="Gauss関数_RGB")
    ax3.legend(loc="upper right", fontsize=10)  # 凡例を自動配置＆フォントサイズ指定
    
    # === Vスケーリングバーの追加 ===
    # 別のAxes（ax_vbar）をグラフ横に追加
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    # === スケールバー（明度 V 0〜1）追加 ===
    # === Vスケーリングバーの追加 ===
    divider = make_axes_locatable(ax3)
    ax_vbar = divider.append_axes("right", size="5%", pad=0.1)

    # ① グラデーション生成（arr_H, arr_S固定で、Vを0→1に変化させた後に上下逆転）
    v_vals = np.linspace(0, 1, 256)
    colors = [colorsys.hsv_to_rgb(arr_H, arr_S, v) for v in v_vals]
    cmap_custom = ListedColormap(colors)

    # === ① グラデーション表示（上下逆転）===
    v_gradient = v_vals[::-1].reshape(-1, 1)  # 
    ax_vbar.imshow(v_gradient, aspect='auto', cmap=cmap_custom)

    # y軸を右側に、上を1.00、下を0.00に
    ax_vbar.yaxis.tick_right()
    ax_vbar.yaxis.set_label_position("right")
    ax_vbar.set_title("V", fontsize=12)    
    # === 目盛り（上:1.00〜下:0.00）を 0.1刻みで表示 ===
    # === y軸の目盛り（0.1刻み）を設定：上が1.00、下が0.00 ===
    v_tick_values = np.arange(1.0, -0.01, -0.1)  # [1.0, 0.9, ..., 0.0]
    yticks = [int((1.0 - v) * 255) for v in v_tick_values]  # V=1.0 → 0（上）, V=0.0 → 255（下）
    yticklabels = [f"{v:.2f}" for v in v_tick_values]
    ax_vbar.set_yticks(yticks)
    ax_vbar.set_yticklabels(yticklabels)
    
    # ② 現在のV位置のインデックス（逆順に合わせて変更）
    #v_index = int(arr_V * 255)  # ← 変更前：(1 - arr_V) * 255
    v_index = int((1 - arr_V) * 255)  # 
    # ② 補色の計算（RGB→補色RGB）
    r, g, b = colorsys.hsv_to_rgb(arr_H, arr_S, arr_V)
    comp_color = (1 - r, 1 - g, 1 - b)  # 補色（RGBの反転）

    # ② 水平線の描画（補色で表示）
    ax_vbar.axhline(v_index, color=comp_color, linewidth=5)

    # x軸目盛りは非表示
    ax_vbar.set_xticks([])

#最適解から色を算出(実際にセロハンテープが生み出せる色)
def fitting_color(keepparams):
    def r_theta(theta):  # 回転行列R(θ）
        return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    def mai_r_theta(theta):  # 回転行列R(-θ）
        return np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])

    def jhons(theta):  # ジョーンズマトリクス
        return np.array([[np.sin(theta)**2, -np.sin(theta)*np.cos(theta)], [-np.sin(theta)*np.cos(theta), np.cos(theta)**2]])
    
    x = np.linspace(380, 750, 371)  # A と B のデータ数を統一
    
    #多変数関数のスペクトルB2(色算出)
    a1, a2, a3 ,a4,a5,a6,a7,a8,a9,a10= keepparams
    
    a2 = round(a2)
    a3 = round(a3)
    a4 = round(a4)
    spcA = []
    spcX =0
    spcY =0
    spcZ =0
    #光路差(各変動-配列値)
    array_ddc1 = [num*(a8/100) for num in np.array(dd)]
    array_ddc2 = [num*(a9/100) for num in np.array(dd)]
    array_ddc3 = [num*(a10/100) for num in np.array(dd)]
    # 偏光板一枚目の回転角
    a = np.deg2rad(-a7)
    E_1 = np.array([[-np.sin(a)], [np.cos(a)]])
    # セロハン二枚目の回転角
    b = np.deg2rad(a6-a7)
    # セロハン三枚目の回転角
    e = np.deg2rad(a5-a7)
    # 偏光板二枚目の回転角
    if a1 == 1: # 直交ニコル配置ver
        c = np.deg2rad(-a7-90)
    elif a1 ==2: # 平行ニコル配置ver
        c = np.deg2rad(-a7)
    elif a1 == 3: # 45°配置ver
        c = np.deg2rad(-a7-45)

    for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
        # 波長
        l = i
        ## 位相差(手前x枚)
        delta = 2*array_ddc1[l-380]*np.pi/l
        ## 位相差(中p枚)
        deltap = 2*array_ddc2[l-380]*np.pi/l
        ## 位相差(奥z枚)
        deltaz = 2*array_ddc3[l-380]*np.pi/l
        # セロハンの項(1jで虚数iを明示的に表現):x枚
        cellox = np.array([[1, 0], [0, np.exp(-1j*delta*a4)]])
        # セロハンの項(1jで虚数iを明示的に表現):p枚
        cellop = np.array([[1, 0], [0, np.exp(-1j*deltap*a3)]])
        # セロハンの項(1jで虚数iを明示的に表現):z枚
        celloz = np.array([[1, 0], [0, np.exp(-1j*deltaz*a2)]])
        # E_2への変換
        E_2 = np.dot(cellox, E_1)
        # E_3への変換
        E_3 = np.dot(r_theta(b), np.dot(
            cellop, np.dot(mai_r_theta(b), E_2)))
        #E_4への変換
        E_4 = np.dot(r_theta(e), np.dot(
            celloz, np.dot(mai_r_theta(e), E_3)))
        # E_5への変換
        E_5 = np.dot(jhons(c), E_4)
        # 各波長でのI(光強度)を算出する
        I = (np.abs(np.abs(E_5[0]**2) + np.abs(E_5[1]**2)))
        #2.強度配列に光源データ配列を積した測定直交スペクトルを算出　
        #3.補正データを積した補正測定直交配置スペクトルを算出
        spc = I*(sp[l-380])
        #4について3種類の等色関数の積の総和をそれぞれ求める /K定数により三刺激値の算出(全座標について)
        cfX = array_cfx[l - 380]
        cfY = array_cfy[l - 380]
        cfZ = array_cfz[l - 380]
        spcX += (spc * cfX * K).item()
        spcY += (spc * cfY * K).item()
        spcZ += (spc * cfZ * K).item()
    
    arr_spcX = spcX #座標の配列(等色関数)について，積の総和を代入
    arr_spcY = spcY
    arr_spcZ = spcZ
    # K定数の修正を行い、三刺激値より色を算出するために、混色比は不必要に。
    #arr_spcXx = (arr_spcX)/((arr_spcX)+(arr_spcY)+(arr_spcZ))
    #arr_spcYy = (arr_spcY)/((arr_spcX)+(arr_spcY)+(arr_spcZ))
    #arr_spcZz = (arr_spcZ)/((arr_spcX)+(arr_spcY)+(arr_spcZ))
    ##三刺激値の行列(3行1列)をE5として作成し，sRGB変換マトリクスとの積を[R"G"B"]配列として算出
    E_5 = np.array([[arr_spcX], [arr_spcY],
                    [arr_spcZ]])  # [[],[],[]三刺激値
    arr_RGB = np.dot(tosRGB, E_5)
    arr_RR= arr_RGB[0]
    arr_GG = arr_RGB[1]
    arr_BB = arr_RGB[2]
    
    def gamma_correction(value):
        if value <= 0.0031308:
            return 12.92 * value * 255
        else:
            return (1.055 * (value ** (1 / 2.4)) - 0.055) * 255

    # ガンマ補正とスケーリングを適用
    arr_RR = gamma_correction(arr_RGB[0].item())
    arr_GG = gamma_correction(arr_RGB[1].item())
    arr_BB = gamma_correction(arr_RGB[2].item())

    # 0〜255 にクリップ
    arr_RR = min(255, max(0, arr_RR))
    arr_GG = min(255, max(0, arr_GG))
    arr_BB = min(255, max(0, arr_BB))
    
    # RGB値をR'G'B'値から算出する．Decimalでstr型で四捨五入(整数)として，.to_integral_valueで数の型にしている
    arr_Rr= float(Decimal(str(arr_RR)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value())
    arr_Gr= float(Decimal(str(arr_GG)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value())
    arr_Br= float(Decimal(str(arr_BB)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value()) 
    #arr_Rr = round(float(arr_RR))
    #arr_Gr = round(float(arr_GG))
    #arr_Br = round(float(arr_BB))
    #RGBの補正へ
    arr_Rr = float(arr_Rr)
    arr_Gr = float(arr_Gr)
    arr_Br = float(arr_Br)
    colorshow=[arr_Rr, arr_Gr, arr_Br]
    return colorshow

# Gauss関数から色を算出(自らが用意したスペクトルが仮に存在する場合の色)
def gauss_color(get_AAA):
    spcX =0
    spcY =0
    spcZ =0
    for i in range(380,751): #各λにおける光路差d対応とジョーンズ・マトリクス計算
        l=i
        spc = (get_AAA[l-380])
        #4について3種類の等色関数の積の総和をそれぞれ求める /K定数により三刺激値の算出(全座標について)
        cfX = array_cfx[l - 380]
        cfY = array_cfy[l - 380]
        cfZ = array_cfz[l - 380]
        spcX += float(spc * cfX * K)
        spcY += float(spc * cfY * K)
        spcZ += float(spc * cfZ * K)
    arr_spcX = spcX #座標の配列(等色関数)について，積の総和を代入
    arr_spcY = spcY
    arr_spcZ = spcZ
    
    #三刺激値から色を算出するために、以下の混色比の算出は不要
    #denominator = arr_spcX + arr_spcY + arr_spcZ
    #if denominator != 0:
        #arr_spcXx = arr_spcX / denominator
        #arr_spcYy = arr_spcY / denominator
        #arr_spcZz = arr_spcZ / denominator
    #else:
        #arr_spcXx = 0
        #arr_spcYy = 0
        #arr_spcZz = 0
        #print("⚠️ スペクトルがすべてゼロです（正規化できません）")
    
    ##混色比の行列(3行1列)をE5として作成し，sRGB変換マトリクスとの積を[R"G"B"]配列として算出
    E_5 = np.array([[arr_spcX], [arr_spcY],
                    [arr_spcZ]])  # [[],[],[]]..?
    arr_RGB = np.dot(tosRGB, E_5)
    arr_RR= arr_RGB[0]
    arr_GG = arr_RGB[1]
    arr_BB = arr_RGB[2]
    
    def gamma_correction(value):
        if value <= 0.0031308:
            return 12.92 * value * 255
        else:
            return (1.055 * (value ** (1 / 2.4)) - 0.055) * 255

    # ガンマ補正とスケーリングを適用
    arr_RR = gamma_correction(arr_RGB[0].item())
    arr_GG = gamma_correction(arr_RGB[1].item())
    arr_BB = gamma_correction(arr_RGB[2].item())

    # 0〜255 にクリップ
    arr_RR = min(255, max(0, arr_RR))
    arr_GG = min(255, max(0, arr_GG))
    arr_BB = min(255, max(0, arr_BB))
    
    # RGB値をR'G'B'値から算出する．Decimalでstr型で四捨五入(整数)として，.to_integral_valueで数の型にしている
    arr_Rr= float(Decimal(str(arr_RR)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value())
    arr_Gr= float(Decimal(str(arr_GG)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value())
    arr_Br= float(Decimal(str(arr_BB)).quantize(Decimal('0'), rounding=ROUND_HALF_UP).to_integral_value()) 

    #RGBの補正へ
    arr_Rr = float(arr_Rr)
    arr_Gr = float(arr_Gr)
    arr_Br = float(arr_Br)
    colorgauss=[arr_Rr, arr_Gr, arr_Br]
    
    return colorgauss



# 初期パラメータ
params = [
    [1.0, 420.0, 30.0],
    [1.0, 536.0, 100.0],
    [1.0, 729.0, 100.0],
    [1.0, 600.0, 100.0]
]
current_gauss = [0]

# GUI構成
root = tk.Tk()
root.geometry("1800x900") 
root.title("Gaussian Spectrum Evaluator")


# 上部にグラフ、下部にUI部品を分ける
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)


# グラフエリア (左右2つ)
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
#canvas = FigureCanvasTkAgg(fig, master=root)
#canvas.get_tk_widget().pack()
canvas = FigureCanvasTkAgg(fig, master=top_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ガウス選択ボタン
button_frame = tk.Frame(root)
button_frame.pack()
for i in range(4):
    tk.Button(button_frame, text=f"Gauss {i+1}", font=("Arial", 16), command=lambda i=i: select_gauss(i)).pack(side=tk.LEFT, padx=5)

current_label = tk.Label(root, text="調整中: Gauss 1", font=("Arial", 14))
current_label.pack()

# スライダー作成
def create_slider(label_text, from_, to, resolution, command,
                with_bounds=False, od_label="",
                with_thickness_bounds=False, thickness_label="",
                with_angle_bounds=False, angle_label=""):
    frame = tk.Frame(bottom_frame, pady=5)
    frame.pack(fill=tk.X)

    tk.Label(frame, text=label_text, font=("Arial", 14), width=10).pack(side=tk.LEFT)

    slider = tk.Scale(
        frame, from_=from_, to=to, orient=tk.HORIZONTAL,
        resolution=resolution, length=400,
        font=("Arial", 12), sliderlength=30, width=20,
        command=command
    )
    slider.pack(side=tk.LEFT, padx=10)

    lower_var, upper_var = None, None
    thick_lower_var, thick_upper_var = None, None
    angle_lower_var, angle_upper_var = None, None

    if with_bounds:
        bounds_input_frame = tk.Frame(frame)
        bounds_input_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(bounds_input_frame, text=f"{od_label} 下限:", font=("Arial", 16)).grid(row=0, column=0)
        lower_var = tk.StringVar(value="240")
        tk.Entry(bounds_input_frame, textvariable=lower_var, font=("Arial", 16), width=6).grid(row=0, column=1)

        tk.Label(bounds_input_frame, text=f"上限:", font=("Arial", 16)).grid(row=0, column=2)
        upper_var = tk.StringVar(value="400")
        tk.Entry(bounds_input_frame, textvariable=upper_var, font=("Arial", 16), width=6).grid(row=0, column=3)

    if with_thickness_bounds:
        thickness_frame = tk.Frame(frame)
        thickness_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(thickness_frame, text=f"{thickness_label} 下限:", font=("Arial", 16)).grid(row=0, column=0)
        thick_lower_var = tk.StringVar(value="1")
        tk.Entry(thickness_frame, textvariable=thick_lower_var, font=("Arial", 16), width=6).grid(row=0, column=1)

        tk.Label(thickness_frame, text=f"上限:", font=("Arial", 16)).grid(row=0, column=2)
        thick_upper_var = tk.StringVar(value="2")
        tk.Entry(thickness_frame, textvariable=thick_upper_var, font=("Arial", 16), width=6).grid(row=0, column=3)

    if with_angle_bounds:
        angle_frame = tk.Frame(frame)
        angle_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(angle_frame, text=f"{angle_label} 下限:", font=("Arial", 16)).grid(row=0, column=0)
        angle_lower_var = tk.StringVar(value="0")
        tk.Entry(angle_frame, textvariable=angle_lower_var, font=("Arial", 16), width=6).grid(row=0, column=1)

        tk.Label(angle_frame, text="上限:", font=("Arial", 16)).grid(row=0, column=2)
        angle_upper_var = tk.StringVar(value="180")
        tk.Entry(angle_frame, textvariable=angle_upper_var, font=("Arial", 16), width=6).grid(row=0, column=3)

    return slider, lower_var, upper_var, thick_lower_var, thick_upper_var, angle_lower_var, angle_upper_var

amp_slider, od1_lower_var, od1_upper_var, od1_thick_lower_var, od1_thick_upper_var, od1_angle_lower_var, od1_angle_upper_var = create_slider(
    "振幅 A:", 0.0, 1.0, 0.1, slider_changed,
    with_bounds=True, od_label="光路差①",
    with_thickness_bounds=True, thickness_label="枚数①",
    with_angle_bounds=True, angle_label="角度①"
)

mu_slider, od2_lower_var, od2_upper_var, od2_thick_lower_var, od2_thick_upper_var, od2_angle_lower_var, od2_angle_upper_var = create_slider(
    "中心 μ:", 280.0, 850.0, 1.0, slider_changed,
    with_bounds=True, od_label="光路差②", with_thickness_bounds=True, thickness_label="枚数②",
    with_angle_bounds=True, angle_label="角度②"
)

sigma_slider, od3_lower_var, od3_upper_var, od3_thick_lower_var, od3_thick_upper_var,od3_angle_lower_var, od3_angle_upper_var = create_slider(
    "幅 σ:", 10, 500.0, 1.0, slider_changed, 
    with_bounds=True, od_label="光路差③", with_thickness_bounds=True, thickness_label="枚数③", 
    with_angle_bounds=True, angle_label="角度③"
)

Intensity_slider, _, _, _, _, _, _ = create_slider("強度 I:", 0, 1.0, 0.01, slider_changed)

# 実行ボタンと評価結果
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

tk.Button(action_frame, text="実行",font=("Arial", 16), command=fitting).pack(side=tk.LEFT, padx=10) # command = 関数名で, その関数を実行する
#tk.Button(action_frame, text="色計算", font=("Arial", 14), command=lambda: fitting_color(keepparams)).pack(side=tk.LEFT, padx=10)
# 「理論値」ボタンを追加
tk.Button(action_frame, text="理論値", font=("Arial", 16), command=fittingGauss).pack(side=tk.LEFT, padx=10)

color_box = tk.Label(action_frame, width=10, height=2, relief=tk.SUNKEN, bg="white")
color_box.pack(side=tk.LEFT, padx=10)

result_label = tk.Label(action_frame, text="RGB: ---")
result_label.pack(side=tk.LEFT, padx=10)

# 最適化結果表示用ラベル 
opt_result_label = tk.Label(action_frame, text="最適化結果: ---", font=("Arial", 14))
opt_result_label.pack(side=tk.LEFT, padx=10)

#追加要素
# 光路差の制約入力フォーム
bounds_frame = tk.Frame(bottom_frame, pady=10)
bounds_frame.pack(fill=tk.X)

def clear_fitting_line_only(*args):
    # 削除したい線のラベル
    fitting_labels_to_remove = ['Fitting Spectrum_直交', 'Fitting Spectrum_平行']

    # 削除対象以外の線だけを保持
    remaining_lines = [
        line for line in ax2.lines
        if line.get_label() not in fitting_labels_to_remove
    ]

    # プロットクリア & 再描画（必要な線のみ）
    ax2.cla()
    for line in remaining_lines:
        ax2.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), color=line.get_color())

    # 軸ラベル・タイトル・凡例再設定
    ax2.set_title("Fitting Plot")
    ax2.set_xlabel("Wavelength")
    ax2.set_ylabel("Intensity")
    ax2.legend()
    canvas.draw()

# 光路差が変更されたときに赤線を削除
od1_lower_var.trace_add("write", clear_fitting_line_only)
od1_upper_var.trace_add("write", clear_fitting_line_only)
od2_lower_var.trace_add("write", clear_fitting_line_only)
od2_upper_var.trace_add("write", clear_fitting_line_only)
od3_lower_var.trace_add("write", clear_fitting_line_only)
od3_upper_var.trace_add("write", clear_fitting_line_only)


# 制約モード切り替えラジオボタン（bottom_frameに配置）
constraint_mode_var = tk.StringVar(value="individual")  # デフォルト: 個別制約

mode_frame = tk.Frame(bottom_frame, pady=5)
mode_frame.pack()

tk.Label(mode_frame, text="制約モード:", font=("Arial", 16)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(mode_frame, text="共通制約", variable=constraint_mode_var, value="common", font=("Arial", 16), command=lambda: update_constraint_mode()).pack(side=tk.LEFT)
tk.Radiobutton(mode_frame, text="個別制約", variable=constraint_mode_var, value="individual", font=("Arial", 16), command=lambda: update_constraint_mode()).pack(side=tk.LEFT)

# --- 光路差③の下に共通制約を置く ---
common_bounds_frame = tk.Frame(bottom_frame, pady=5)
common_bounds_frame.pack(fill=tk.X)

tk.Label(common_bounds_frame, text="共通制約 下限:", font=("Arial", 16)).pack(side=tk.LEFT, padx=(20, 5))
common_lower_var = tk.StringVar(value="240")
tk.Entry(common_bounds_frame, textvariable=common_lower_var, font=("Arial", 16), width=6).pack(side=tk.LEFT)

tk.Label(common_bounds_frame, text="上限:", font=("Arial", 16)).pack(side=tk.LEFT, padx=(20, 5))
common_upper_var = tk.StringVar(value="400")
tk.Entry(common_bounds_frame, textvariable=common_upper_var, font=("Arial", 16), width=6).pack(side=tk.LEFT)

# ---直交-平行に関する要素---
polarization_mode_var = tk.StringVar(value="orthogonal")

polarization_frame = tk.Frame(bottom_frame, pady=5)
polarization_frame.pack()

tk.Label(polarization_frame, text="偏光モード:", font=("Arial", 16)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(polarization_frame, text="直交", variable=polarization_mode_var, value="orthogonal", font=("Arial", 16), command=lambda: update_polarization_mode()).pack(side=tk.LEFT)
tk.Radiobutton(polarization_frame, text="平行", variable=polarization_mode_var, value="parallel", font=("Arial", 16), command=lambda: update_polarization_mode()).pack(side=tk.LEFT)


# 初期状態では非表示にしておく
common_bounds_frame.pack_forget()

def update_constraint_mode():
    mode = constraint_mode_var.get()

    if mode == "common":
        common_bounds_frame.pack(fill=tk.X)

        val_low = common_lower_var.get()
        val_up = common_upper_var.get()
        od1_lower_var.set(val_low)
        od1_upper_var.set(val_up)
        od2_lower_var.set(val_low)
        od2_upper_var.set(val_up)
        od3_lower_var.set(val_low)
        od3_upper_var.set(val_up)
    else:
        common_bounds_frame.pack_forget()


def update_polarization_mode():
    mode = polarization_mode_var.get()
    mode = polarization_mode_var.get()
    if mode == "orthogonal":# 直交時
        P_plate =1
        
    elif mode == "parallel": #平行時
        P_plate=2


# 共通制約の下限と上限が変更されたときにも赤線を削除
common_lower_var.trace_add("write", clear_fitting_line_only)
common_upper_var.trace_add("write", clear_fitting_line_only)

# 初期表示
select_gauss(0)
update_plot()

root.mainloop()
print("ウィンドウを閉じました")




