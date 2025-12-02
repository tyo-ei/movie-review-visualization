import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ===== 字体设置 =====
font_path = "NotoSansJP-Regular.ttf"  

# 把字体文件注册到 matplotlib 的字体管理器中
font_manager.fontManager.addfont(font_path)

# 这里用字体家族名作为全局字体
plt.rcParams["font.family"] = "Noto Sans JP"
plt.rcParams["axes.unicode_minus"] = False


# ===== 读取总分析结果 =====
df = pd.read_csv("analysis_all.csv")

st.title("映画レビュー多面的評価の可視化システム")

# 电影列表
movies = sorted(df["movie"].unique())
selected_movie = st.selectbox("作品を選択してください", movies)

# 只取选中的电影
film_df = df[df["movie"] == selected_movie]

# 按側面计算平均分
order = ["ストーリー", "演技", "映像効果", "音響"]
aspect_mean = film_df.groupby("aspect")["sentiment"].mean()
aspect_mean = aspect_mean.reindex(order)
aspect_mean = aspect_mean.fillna(0)  # 防止某个側面没有数据时报错

# ===== 柱状图 =====
st.subheader(f"{selected_movie} の各側面の平均スコア（柱状図）")

fig1, ax1 = plt.subplots()
ax1.bar(aspect_mean.index, aspect_mean.values)
ax1.set_ylim(0, 1)
ax1.set_ylabel("平均スコア")
ax1.set_xlabel("側面")
st.pyplot(fig1)

# ===== 雷达图 =====
st.subheader(f"{selected_movie} の各側面のバランス（レーダーチャート）")

labels = aspect_mean.index.tolist()
values = aspect_mean.values.tolist()
num_vars = len(labels)

# 角度 & 闭合
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

fig2, ax2 = plt.subplots(subplot_kw=dict(polar=True))
ax2.plot(angles, values)
ax2.fill(angles, values, alpha=0.25)

ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(labels)
ax2.set_ylim(0, 1)

st.pyplot(fig2)




