# 地図作成ライブラリのインポート
import folium

# マップオブジェクト作成

map = folium.Map(location=[35.35, 137.37], zoom_start=14)



# 避難所の座標
#山岡中
chu = [35.35572, 137.374904]
folium.Marker(
    location=chu,
    popup="山岡中学校・体育館",
    icon=folium.Icon(color='blue')
).add_to(map)

#山岡小
syo = [35.35579, 137.382441]
folium.Marker(
    location=syo,
    popup="山岡小学校・体育館",
    icon=folium.Icon(color='blue')
).add_to(map)

#山岡B&G海洋センター・体育館
bg = [35.353073, 137.376396]
folium.Marker(
    location=bg,
    popup="山岡B&G海洋センター",
    icon=folium.Icon(color='blue')
).add_to(map)

#山岡農村環境改善センター・ホール
kankyo = [35.351983, 137.381231]
folium.Marker(
    location=kankyo,
    popup="山岡農村環境改善センター",
    icon=folium.Icon(color='blue')
).add_to(map)

#爪切地蔵ふれあい会館・ホール
tsumekiri = [35.369331, 137.39361]
folium.Marker(
    location=tsumekiri,
    popup="爪切地蔵ふれあい会館",
    icon=folium.Icon(color='blue')
).add_to(map)

#原公民館・ホール
hara = [35.330214, 137.355363]
folium.Marker(
    location=hara,
    popup="原公民館",
    icon=folium.Icon(color='blue')
).add_to(map)

#田代集落農事集会所・ホール
tasiro = [35.338784, 137.323822]
folium.Marker(
    location=tasiro,
    popup="田代集落農事集会所",
    icon=folium.Icon(color='blue')
).add_to(map)

#釜屋公孫樹会館・ホール
kamaya = [35.337339, 137.373532]
folium.Marker(
    location=kamaya,
    popup="釜屋公孫樹会館",
    icon=folium.Icon(color='blue')
).add_to(map)

#ひまわり会館・ホール
himawari = [35.345164, 137.395606]
folium.Marker(
    location=himawari,
    popup="ひまわり会館",
    icon=folium.Icon(color='blue')
).add_to(map)

#さくら会館・ホール
sakura = [35.355814, 137.408057]
folium.Marker(
    location=sakura,
    popup="さくら会館",
    icon=folium.Icon(color='blue')
).add_to(map)



# 保存
map.save("避難所.html")

# 表示
map
