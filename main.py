import flet as ft
from flet import Page, AppBar, TextField, Image, FilledButton, Text, IconButton, Container
import requests
# USE ALTSTORE TO PUBLISH TO IOS

ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
symbols = ["s"]

base = 'https://nftstorage.link/ipfs/bafybeibs6d5wjelj7aomlaegvm472j3nylrzvfakopbft3a2pyjkwzrl2y/'
imgs = [base+'s0g.jpg', base+'s0r.jpg',
        base+'s0b.jpg']

imgsIndexToColor = {0: 'g', 1: 'r', 2: 'b'}
colorToImgsIndex = {'g': 0, 'r': 1, 'b': 2}
numToRanks = {'11': 'j', '12': 'q', '13': 'k'}

cardSrc = [base+'s0g.jpg']

for s in symbols:
    for r in ranks:
        cardSrc.append(base + s + r + 'g' + ".jpg")

payout = 1
balance = 100
bet = 1
lastCon = None
sequence = ['00', '00', '00', '00', '00']
server = 'https://0037-141-147-29-255.ngrok-free.app/'


def main(page: Page):

    def getPayout():
        global sequence
        p = 1
        for s in sequence:
            if s[0] != '0':
                p *= 10
            if s[1] != '0':
                p *= 1.9
        return p


    def to_main():
        page.views.pop()
        page.go("/")

    def save_card(event):
        global lastCon
        global payout
        container = event.control

        imgIndex = str(cardSrc.index(container.content.src))
        if int(imgIndex) > 10:
            imgIndex = numToRanks[imgIndex]

        containerIndex = icons.index(lastCon)
        sequence[containerIndex] = imgIndex + sequence[containerIndex][-1]

        src = lastCon.content.src
        src = src[len(base):len(src) - 4]
        imgIndexColor = 0
        if src.__contains__('r'):
            imgIndexColor = 1
        elif src.__contains__('b'):
            imgIndexColor = 2
        #imgIndexColor = imgs.index(lastCon.content.src)
        color = imgsIndexToColor[imgIndexColor]
        src = lastCon.content.src

        src = src[len(base):len(src) - 4]
        if len(src) == 4:
            src = src[2]
        else:
            src = src[1]
        lastCon.content.src = base + s[0] + imgIndex + color + '.jpg'
        payout = getPayout()
        payout = round(payout, 2)
        topBar[1] = ft.Text(f"payout: {payout}x", size=20, expand=True)
        to_main()

    def to_card_chooser(event):
        global payout
        global lastCon
        container = event.control

        containerIndex = icons.index(container)

        lastCon = container
        src = container.content.src
        src = src[len(base):len(src)-4]
        imgIndex = 2
        if src.__contains__('r'):
            imgIndex = 0
        elif src.__contains__('b'):
            imgIndex = 1

        src = src[:-1] + imgsIndexToColor[imgIndex]

        sequence[containerIndex] = sequence[containerIndex][:-1] + imgsIndexToColor[imgIndex]
        if imgsIndexToColor[imgIndex] == 'g':
            sequence[containerIndex] = sequence[containerIndex][:-1] + '0'

        container.content.src = base + src + '.jpg' # imgs[newImgIndex]


        payout = getPayout()
        payout = round(payout, 2)
        topBar[1] = ft.Text(f"payout: {payout}x", size=20, expand=True)
        page.go("/chooser")

    def route_change(route):
        if page.route == "/chooser":
            cardImgs = []
            for src in cardSrc:
                    cardImgs.append(Container(content=Image(src=src), on_click=save_card))

            page.views.append(
                ft.View(
                    "/chooser",
                    [
                        ft.Row(cardImgs, ft.MainAxisAlignment.SPACE_BETWEEN, scroll=ft.ScrollMode.ALWAYS, wrap=True)
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change

    topBar = [ft.Text(f"balance: {balance}$", size=20, expand=True),
              ft.Text(f"payout: {payout}x", size=20, expand=True),
              ft.Text(f"bet: {bet}$", size=20, expand=True)]

    icons = [Container(content=Image(src=imgs[0]), expand=True, on_click=lambda x: switchColor(x), on_long_press=to_card_chooser) for _ in range(5)]
    winners = [Container(content=Image(src=imgs[0]), expand=True) for _ in range(5)]

    def switchColor(event):
        global payout
        global lastCon

        container = event.control

        #find index of container
        containerIndex = icons.index(container)

        src = container.content.src
        srcE = src[len(base):len(src) - 4]
        imgIndex = 0

        if srcE.__contains__('r'):
            imgIndex = 1
            srcE = srcE[:-1] + 'b'
            sequence[containerIndex] = sequence[containerIndex][:-1] + 'b'
        elif srcE.__contains__('b'):
            imgIndex = 2
            srcE = srcE[:-1] + 'g'
            sequence[containerIndex] = sequence[containerIndex][:-1] + '0'
        else:
            srcE = srcE[:-1] + 'r'
            sequence[containerIndex] = sequence[containerIndex][:-1] + 'r'

        container.content.src = base + srcE + '.jpg'
        lastCon = container

        payout = getPayout()
        payout = round(payout, 2)

        topBar[1] = ft.Text(f"payout: {payout}x", size=20, expand=True)

        page.update()

    def play():
        global server
        global balance
        user = 'admin'
        password = 'admin'
        wager = str(10)
        bet = ''.join(sequence)
        PARAMS = {'user':user, 'pass':password, 'wager':wager, 'bet':bet}
        r = requests.get(url=server + '/play', params=PARAMS)
        data = r.json()
        balance = round(int(data[2]), 2)
        topBar[0] = ft.Text(f"balance: {balance}$", size=20, expand=True)
        winnerSequence = data[0]
        for i, winner in enumerate(winnerSequence):
            winners[i].content.src = base + symbols[0] + winner + '.jpg'
        page.update()


    playBtn = FilledButton(text="play", on_click= lambda _: play())

    page.add(
        ft.Row(
            topBar,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row(
            icons,
            ),
        ft.Row(
            winners,
            ),
        playBtn
    )


ft.app(target=main)

"""
when sending request to the API we will use these values as bet
card: ranking color
ranking: 1-k
color: b-r
none: 0
blue, red 8, ., red, .
bet: 0br800r000

response shall be in the same way


"""
