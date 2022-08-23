import pandas as pd
from flask import Flask, render_template, url_for, redirect
import folium
import json
import requests
import config
import pandas as pd
from flask import Flask, render_template, url_for
import requests
from flask import *
from SPARQLWrapper import SPARQLWrapper
import pickle
import re
from flask import Flask, render_template, request
import requests
from datetime import datetime
import openrouteservice
from branca.element import Figure
from openrouteservice import convert




dosya_k = 0
dosya_c = 0
sinsui_k = 0
sinsui_c = 0
ena = "2121000"

df=pd.read_csv("enahinan2.csv")

    


# 保存
#map.save("恵那市避難所.html")

app = Flask(__name__)

"""
@app.route('/', methods=['GET'])
def postnum():
    
        
    return render_template('sample.html')
"""
@app.route("/")
def root():
    return redirect("normal")

@app.route('/normal')
def postnum1():
    if request.args.get("ido_src") is not None and request.args.get("kei_src") is not None and request.args.get("ido_dst") is not None and request.args.get("kei_dst") is not None:
        ido_src = request.args.get("ido_src")
        kei_src = request.args.get("kei_src")
        ido_dst = request.args.get("ido_dst")
        kei_dst = request.args.get("kei_dst")
        p1 = float(ido_src), float(kei_src)
        p2 = float(ido_dst), float(kei_dst)
        p1r = tuple(reversed(p1))
        p2r = tuple(reversed(p2))
        mean_lat = (p1[0] + p2[0]) / 2
        mean_long = (p1[1] + p2[1]) / 2

        folium_map = folium.Map(location=(mean_lat, mean_long), zoom_start=14)#定義

        key = "5b3ce3597851110001cf6248777fde52d32b43ecbdf3f8ffc6d81120"
        client = openrouteservice.Client(key=key)
        #res = "L.marker([" + ido + "," + kei + "]).addTo(map)"

            # 経路計算 (Directions V2)
        routedict = client.directions((p1r, p2r),profile="foot-walking")
        geom = routedict["routes"][0]["geometry"]
        decoded = convert.decode_polyline(geom)

        # 上の計算の続きで

        def reverse_lat_long(list_of_lat_long):
            """緯度経度をひっくり返す"""
            return [(p[1], p[0]) for p in list_of_lat_long]

        coord = reverse_lat_long(decoded["coordinates"])

        # 位置情報をPolyLineで地図に追加
        folium.vector_layers.PolyLine(locations=coord).add_to(folium_map)
        
        return folium_map._repr_html_()
    else:
        return render_template("sample4.html")
    
@app.route("/alert")
def alert():
    
    dosya_k = 0
    dosya_c = 0
    sinsui_k = 0
    sinsui_c = 0
    df = pd.read_csv("enahinan2.csv")
    
    f = open("gifu.json", encoding="utf-8")
    tmp = f.read()
    jsn = json.loads(tmp)
    """

    url = "https://www.jma.go.jp/bosai/warning/data/warning/210000.json"
    res = requests.get(url)
    jsn = json.loads(res.text)
    """
    #地図の中心


    def confirm_aqc(data:list) -> str:
      
              if data[1] == 0:
                return str(data[0])
              else:
                return "品質情報を確認して下さい"


    def find_index(data:list, code:str) -> int:
            
              """
              対象のエリアのデータが格納されているインデックス番号を返す
              input : list
              return : int
              """
              index = [num for num, i in enumerate(data) if i["area"]["code"] == code][0]
              return index
    #降水量情報取得
    json_open = open('ame.json', 'r',encoding='utf-8')
    amedas_data = json.load(json_open)
    latest_key = max(amedas_data)
    latest_precipitation1h = confirm_aqc(amedas_data[latest_key]["precipitation1h"])
    
    #恵那市の災害情報取得
    for i in range(len(jsn['areaTypes'][1]["areas"])):
        
    #print(jsn['areaTypes'][1]["areas"][i]["code"])
        if jsn['areaTypes'][1]["areas"][i]["code"] == ena:
            if ("warnings" in jsn['areaTypes'][1]["areas"][i]) == True:
            #print(jsn['areaTypes'][1]["areas"][i]["warnings"][0]["attentions"][0]);
                for j in range(len(jsn['areaTypes'][1]["areas"][i]["warnings"])):
                    #d = jsn['areaTypes'][1]["areas"][i]["warnings"][j]
                    if ("attentions" in jsn['areaTypes'][1]["areas"][i]["warnings"][j]) == True:
                        #attentionsが存在したら、警戒情報を取得
                        for m in range(len(jsn['areaTypes'][1]["areas"][i]["warnings"][j]["attentions"])):
                            
                             if (jsn['areaTypes'][1]["areas"][i]["warnings"][j]["attentions"][m]) == '土砂災害警戒':
                                 dosya_k+=1 #土砂警戒+1
                                 i1=i
                                 j1=j
                                 m1=m
                                 tex1 = "土砂災害警戒"
                                 
                             if (jsn['areaTypes'][1]["areas"][i]["warnings"][j]["attentions"][m]) == '土砂災害注意':
                                 dosya_c+=1
                                 i1=i
                                 j1=j
                                 m1=m
                                 tex1 = "土砂災害注意"
                            
                             if (jsn['areaTypes'][1]["areas"][i]["warnings"][j]["attentions"][m]) == '浸水警戒':
                                 sinsui_k+=1
                                 i1=i
                                 j1=j
                                 m1=m
                                 tex2 = "浸水警戒"
                        
                             if (jsn['areaTypes'][1]["areas"][i]["warnings"][j]["attentions"][m]) == '浸水注意':
                                 sinsui_c+=1
                                 i1=i
                                 j1=j
                                 m1=m
                                 tex2 ="浸水注意"
                                 
    #土砂災害の場合避難所表示
    if int(latest_precipitation1h) >= 94:
        dfa = df.query("洪水==1")
        ido = dfa["緯度"].values
        kei = dfa["経度"].values
        text = "記録的な大雨が発生中"
        text1 = ""
        res = ""
        for i in range(len(ido)):
            
            res = res + "\tL.marker(["+str(ido[i])+","+str(kei[i])+"]).bindPopup(\""+df["名称"][i]+"\").addTo(map);\n"

        if dosya_k>=1:
            text1 = "土砂災害警戒発令中"

        if dosya_c>=1:
            text1 = "土砂災害注意報発令中"
        return render_template('sample4.html', res = res, text = text, text1=text1)
        
        
    
    elif dosya_k>=1:
        dfa = df.query("土砂災害==1")
        ido = dfa["緯度"].values
        kei = dfa["経度"].values
        text =tex1 + "発令中"
        res = ""
        for i in range(len(ido)):
            
            res = res + "\tL.marker(["+str(ido[i])+","+str(kei[i])+"]).bindPopup(\""+df["名称"][i]+"\").addTo(map);\n"
        return render_template('sample4.html', res = res,text=text)

    elif dosya_c>=1:
        dfa = df.query("土砂災害==1")
        ido = dfa["緯度"].values
        kei = dfa["経度"].values
        text =tex1
        res = ""
        for i in range(len(ido)):
            
            res = res + "\tL.marker(["+str(ido[i])+","+str(kei[i])+"]).bindPopup(\""+df["名称"][i]+"\").addTo(map);\n"
        return render_template('sample4.html', res = res,text=text)

    else:
        
        return redirect("normal")

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost') 



    






