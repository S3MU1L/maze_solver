import tkinter
import queue
smery = [0,1,0,-1]
smerx = [-1,0,1,0]
WIDTH = 630
HEIGHT = 630
TILE_SIZE = 30
N = 600//TILE_SIZE
w = 600
root = tkinter.Tk()
canvas = tkinter.Canvas(root ,width = WIDTH, height = HEIGHT, bg = 'white')
pocet = 0
zaciatok = (0, 0)
koniec = (0, 0)
visited = []
previous = []
obstacles = []
pressed = False

def kresli_ciary():
    for y in range(TILE_SIZE, w+1, TILE_SIZE):
        canvas.create_line(TILE_SIZE, y, w, y, fill='black')
    for x in range(TILE_SIZE, w+1, TILE_SIZE):
        canvas.create_line(x, TILE_SIZE, x, w, fill='black')

for i in range(N):
    visited.append(N * [False])
    previous.append(N * [-1])
    obstacles.append(N * ['.'])
kresli_ciary()


def restart():
    global pocet,zaciatok,koniec,pressed,visited,previous,obstacles
    canvas.delete('all')
    pocet = 0
    zaciatok = (0, 0)
    koniec = (0, 0)
    visited = []
    previous = []
    obstacles = []
    pressed = False
    for i in range(N):
        visited.append(N * [False])
        previous.append(N * [-1])
        obstacles.append(N * ['.'])
    kresli_ciary()


def move(event):
    global pocet
    global obstacles
    x = event.x
    y = event.y
    i = x // TILE_SIZE
    j = y // TILE_SIZE
    if pocet==2 and x>=TILE_SIZE and x<=w and y>=TILE_SIZE and y<=w and (i-1,j-1)!=koniec and (i-1,j-1)!=zaciatok :
        canvas.create_rectangle(i * TILE_SIZE, j * TILE_SIZE, i * TILE_SIZE + TILE_SIZE, j * TILE_SIZE + TILE_SIZE, fill="red")
        obstacles[i - 1][j - 1] = '#'

def click(event):
    global pocet
    global zaciatok
    global koniec
    global obstacles
    x = event.x
    y = event.y

    if x<TILE_SIZE or x>w or y<TILE_SIZE or y>w:
        return

    i = x//TILE_SIZE
    j = y//TILE_SIZE

    if pocet<2 or (i-1,j-1)==koniec or (i-1,j-1)==zaciatok:
        color = 'green'
    else:
        color = 'red'

    canvas.create_rectangle(i*TILE_SIZE,j*TILE_SIZE,i*TILE_SIZE+TILE_SIZE,j*TILE_SIZE+TILE_SIZE,fill = color)


    if pocet == 0:
        zaciatok = (i-1,j-1)
        pocet+=1
    elif pocet == 1:
        koniec = (i-1,j-1)
        pocet+=1
    else:
        obstacles[i-1][j-1]='#'


def draw_sol():
    for j in range(len(obstacles)):
        for i in range(len(obstacles[j])):
            if obstacles[i][j]=='#':
                print(i,j)
    global koniec
    Q = queue.Queue()
    Q.put(zaciatok)
    visited[zaciatok[0]][zaciatok[1]]==True
    while(not Q.empty()):
        front = Q.get()
        x = front[0]
        y = front[1]
        visited[x][y]=True
        for i in range(4):
            dx = x + smerx[i]
            dy = y + smery[i]
            if visited[dx][dy]:
                continue
            if obstacles[dx][dy]=='#':
                continue
            if dx<0 or dx>=19 or dy<0 or dy>=19:
                continue

            visited[dx][dy]=True
            previous[dx][dy]=i
            if (dx,dy)==koniec:
                break
            Q.put((dx,dy))
    if visited[koniec[0]][koniec[1]]:
        a = previous[koniec[0]][koniec[1]]
        koniec = (koniec[0] - smerx[a], koniec[1] - smery[a])
        while koniec != zaciatok:
            i = koniec[0]+1
            j = koniec[1]+1
            canvas.create_rectangle(i*TILE_SIZE,j*TILE_SIZE,i*TILE_SIZE+TILE_SIZE,j*TILE_SIZE+TILE_SIZE,fill = "blue")
            a = previous[koniec[0]][koniec[1]]
            koniec = (koniec[0]-smerx[a],koniec[1]-smery[a])
    else:
        print("Neda sa")

button = tkinter.Button(root, text = "SOLVE", fg = "red", command = draw_sol)
res = tkinter.Button(root,text = "restart",command = restart,fg = "red")
canvas.bind('<Button-1>',click)
canvas.bind('<B1-Motion>',move)
canvas.grid(row = 0, column = 0,columnspan=2)
button.grid(row = 1, column = 0)
res.grid(row = 1, column = 1)

root.mainloop()