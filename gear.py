# Cango Spur Gears
from browser import document as doc
from browser import html
import math
canvas = html.CANVAS(width = 600, height = 400)
canvas.id = "cango_gear"
brython_div = doc["brython_div"]
brython_div <= canvas
from browser import document as doc
from browser import window
import math

canvas = doc["cango_gear"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
cango = window.Cango.new
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
shape = window.Shape.new
path = window.Path.new
creategeartooth = window.createGearTooth.new

tweener = window.Tweener.new
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="cango_gear" 的 canvas 上
cgo = cango("cango_gear")

######################################
# 畫正齒輪輪廓
#####################################
def cangoGear(n, m, pa):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
    gearTooth = path(data, {
      "fillColor":"#ddd0dd",
      "border": True,
      "strokeColor": "#606060" })
    gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)

    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        gear.appendPath(newTooth)
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = path(shapedefs.circle(hr), {
      "fillColor":"#ddd0dd",
      "border": True,
      "strokeColor": "#606060" })
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    return gear

# 設定兩齒齒數
n1 = 17
n2 = 11
n3 = 13
reduced_ratio = 0.5
# 使用 80% 的畫布寬度
m = 0.8*canvas.width/((n1+n2+n3)*reduced_ratio)
# 設定共同的壓力角
pa = 25
# n 齒輪的節圓半徑
pr1 = n1*m/2
# n2 齒輪的節圓半徑
pr2 = n2*m/2
pr3 = n3*m/2

r1 = 0
r2 = (180 + 360 / n2 / 2) + r1 * n1 / n2
r3 = (180 + 360 / n3 / 2) + r2 * n2 / n3

cx = canvas.width/2
cy = canvas.height/2
# 建立 gears
gear1 = cangoGear(n1, m, pa)
gear2 = cangoGear(n2, m, pa)
gear3 = cangoGear(n3, m, pa)

from browser.timer import set_interval

deg = math.pi/180
rotate_speed = 12*deg

def draw():
    cgo.clearCanvas()
    gear1.transform.translate(cx, cy)
    gear1.transform.scale(reduced_ratio)
    gear1.transform.rotate(r1)
    gear1.rotate(rotate_speed)
    cgo.render(gear1)
    
    gear2.transform.translate(cx + (pr1 + pr2) * reduced_ratio, cy)
    gear2.transform.scale(reduced_ratio)
    gear2.transform.rotate(r2)
    gear2.rotate(-rotate_speed * n1 / n2)
    cgo.render(gear2)
    
    gear3.transform.translate(cx + (pr1 + pr2 + pr3) * reduced_ratio, cy)
    gear3.transform.scale(reduced_ratio)
    gear3.transform.rotate(r3)
    gear3.rotate(rotate_speed * n1 / n2 * n2 / n3)
    cgo.render(gear3)

set_interval(draw, 2)
