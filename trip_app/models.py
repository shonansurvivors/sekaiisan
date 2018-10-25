import random
import re
from time import sleep

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import IntegrityError
import requests

from .bing import Bing


class SiteMaster(models.Model):
    description = models.TextField(verbose_name='サイト説明文', blank=True, null=True)
    contact_form_utl = models.URLField(verbose_name='お問い合わせフォームURL', blank=True, null=True)
    dummy = models.TextField(verbose_name='dummy', blank=True, null=True)


class Country(models.Model):
    formal_name = models.CharField(verbose_name='正式名称', max_length=255, blank=True, null=True)
    area_choices = (
        ('EU', 'ヨーロッパ'),
        ('AS', 'アジア'),
        ('NA', '北米・中米'),
        ('SA', '南米'),
        ('OC', 'オセアニア'),
        ('AF', 'アフリカ'),
    )
    area = models.CharField(verbose_name='地域', max_length=2, choices=area_choices, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self):
        return self.formal_name


class Heritage(models.Model):
    formal_name = models.CharField(verbose_name='名称', max_length=255)
    country = models.ForeignKey(Country, verbose_name='国', on_delete=models.SET_NULL, null=True)
    regex = models.CharField('正規表現', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('formal_name',)

    def __str__(self):
        return self.formal_name

    @classmethod
    def scraping_all(cls):

        urls = [
            'http://www.unesco.or.jp/isan/list/europe_1/',
            'http://www.unesco.or.jp/isan/list/europe_2/',
            'http://www.unesco.or.jp/isan/list/europe_3/',
            'http://www.unesco.or.jp/isan/list/asia_1/',
            'http://www.unesco.or.jp/isan/list/asia_2/',
            'http://www.unesco.or.jp/isan/list/america_1/',
            'http://www.unesco.or.jp/isan/list/america_2/',
            'http://www.unesco.or.jp/isan/list/oceania/',
            'http://www.unesco.or.jp/isan/list/africa/',
        ]

        for url in urls:

            print(url)
            sleep(1)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            element_tags = soup.find_all('th')

            for element_tag in element_tags:

                if element_tag.text == '遺跡名称':
                    continue

                # 項番かどうか判定
                if len(element_tag.text) <= 2:
                    continue

                if re.search('登録削除', element_tag.text):
                    continue

                # 世界遺産名をURLに含めている為、半角スラッシュを全角に変換しておく
                heritage_name = element_tag.text.rstrip().replace('/', '／')

                try:
                    heritage = cls.objects.get(formal_name=heritage_name)
                except ObjectDoesNotExist:
                    heritage = Heritage()
                    heritage.formal_name = heritage_name

                try:
                    country_name = element_tag.find_parent().find_parent().find_parent('table')['summary']

                    try:
                        country = Country.objects.get(formal_name=country_name)
                    except ObjectDoesNotExist:
                        country = Country()

                    country.formal_name = country_name

                    if 'europe' in url:
                        country.area = 'EU'
                    elif 'asia' in url:
                        country.area = 'AS'
                    elif 'america_1' in url:
                        country.area = 'NA'
                    elif 'america_2' in url:
                        country.area = 'SA'
                    elif 'oceania' in url:
                        country.area = 'OC'
                    elif 'africa' in url:
                        country.area = 'AF'
                    else:
                        country.area = None

                    country.save()

                    heritage.country = country

                except TypeError:
                    pass

                heritage.save()

        cls.update_regex_all()

    @classmethod
    def update_regex_all(cls):

        heritages = cls.objects.all()

        with open('heritage.txt', 'w', encoding='UTF-8') as f:

            for heritage in heritages:

                t = heritage.formal_name

                t = t.replace('アルカラ・デ・エナレスの大学と歴史地区', 'アルカラ・デ・エナレスの大学')
                t = t.replace('を含むスタッドリー王立公園', '、スタッドリー王立公園')
                t = t.replace('スピシュスキー城及びその関連する文化財', 'スピシュスキー城')
                t = t.replace('ベリンツォーナ旧市街にある3つの城、要塞及び城壁',
                              'ベリンツォーナ旧市街、カステルグランデ、モンテベッロ城、サッソ・コルバロ城')
                t = t.replace('オフリド地域の自然遺産及び文化遺産', 'オフリド地域の自然遺産及びオフリド地域の文化遺産')
                t = t.replace('デルベントのシタデル、古代都市、要塞建築物群', 'デルベントのシタデル、アレクサンドロスの門')
                t = t.replace('ポーランド、ウクライナのカルパチア地方の木造教会', 'カルパチア地方の木造教会')
                # ルルーはレンタルルームなどにヒットする為、削除
                t = t.replace('及びル・ルー（エノー）', '')
                t = t.replace('ネースヴィジのラジヴィール家の建築、住居、文化的複合体', 'ネースヴィジのラジヴィール家')
                # バットは野球のバットなどにヒットする為、削除
                t = t.replace('バット、アル-フトゥム、アル-アインの古代遺跡群', 'アル-フトゥム、アル-アイン')
                t = t.replace('明治日本の産業革命遺産　製鉄・製鋼、造船、石炭産業', '明治日本の産業革命遺産')
                t = t.replace('平泉-仏国土（浄土）を表す建築・庭園及び考古学的遺跡群', '平泉')
                t = t.replace('ポルトヴェネーレ、チンクエ・テッレ及び小島群（パルマリア、ティーノ及びティネット島）',
                              'ポルトヴェネーレ、チンクエ・テッレ、パルマリア、ティーノ、ティネット')
                t = t.replace('アントニ・ガウディの作品群', 'ガウディ')
                t = t.replace('法隆寺地域の仏教建造物', '法隆寺')
                t = t.replace('琉球王国のグスク及び関連遺産群', '琉球王国のグスク')
                t = t.replace('アウシュヴィッツ・ビルケナウ　ナチスドイツの強制絶滅収容所（1940 - 1945）',
                              'アウシュヴィッツ・ビルケナウ　ナチスドイツの強制絶滅収容所')
                t = t.replace('ケニア山国立公園／自然林', 'ケニア山国立公園')

                t = t.replace('アルカラ・デ・エナレスの大学と歴史地区', 'アルカラ・デ・エナレスの(大学|歴史地区)')
                t = t.replace('アンティグアの海軍造船所と関連考古遺跡群', 'アンティグアの(海軍造船所|関連考古遺跡群)')
                t = t.replace('イェリング墳墓群、ルーン文字石碑群と教会', 'イェリング墳墓群、ルーン文字石碑群')
                t = t.replace('イエス生誕の地：ベツレヘムの聖誕教会と巡礼路', 'イエス生誕の地：ベツレヘムの(聖誕教会|巡礼路)')
                t = t.replace('イビサ、生物多様性と文化', 'イビ(サ|ザ)')
                t = t.replace('エチミアツィンの大聖堂と教会群及びズヴァルトノツの古代遺跡',
                              'エチミアツィンの大聖堂及びズヴァルトノツの古代遺跡')
                t = t.replace('エディンバラの旧市街と新市街', 'エ(ディ|ジ)ンバラの(旧市街|新市街)')
                t = t.replace('エルサレムの旧市街とその城壁群', 'エルサレムの(旧市街|城壁群)')
                t = t.replace('エーランド島南部の農業景観', 'エーランド島')
                t = t.replace('オランジュのローマ劇場とその周辺及び“凱旋門”', 'オランジュのローマ劇場及び凱旋門')
                t = t.replace('オールド・ハバナとその要塞群', 'オールド・ハバナ')
                t = t.replace('カザン・クレムリンの歴史遺産群と建築物群', 'カザン・クレムリン')
                t = t.replace('カゼルタの18世紀の王宮と公園、ヴァンヴィテッリの水道橋とサン・レウチョ邸宅群',
                              'カゼルタ|ヴァンヴィテッリ|サン・レウチョ')
                t = t.replace('カリフォルニア湾の島々と保護地域群', 'カリフォルニア湾の(島々|保護地域群)')
                t = t.replace('カルヴァリア・ゼブジトフスカ：マニエリスム様式の建築と公園の景観複合体と巡礼公園',
                              'カルヴァリア・ゼブジトフスカ：マニエリスム様式の(建築|公園の景観複合体|巡礼公園)')
                t = t.replace('カンペチェ州カラクムルの古代マヤ都市と熱帯保護林',
                              '(カンペチェ州)?カラクムル、古代マヤ')
                t = t.replace('カールスクローナの軍港', 'カールスクローナ')
                # todo
                t = t.replace('キリグアの遺跡公園と遺跡群', 'キリグアの(遺跡公園|遺跡群)')
                t = t.replace('クロミェルジーシュの庭園群と城', 'クロミェルジーシュ')
                # todo
                t = t.replace('クンタ・キンテ島と関連遺跡群', 'クンタ・キンテ島')
                t = t.replace('クヴェートリンブルクの聖堂参事会教会、城と旧市街',
                              'クヴェートリンブルクの(聖堂参事会教会|城|旧市街)')
                # todo
                t = t.replace('グウィネズのエドワード１世の城群と市壁群', 'グウィネズのエドワード１世の(城群|市壁群)')
                # todo
                t = t.replace('ケルクアンの古代カルタゴの町とその墓地遺跡', 'ケルクアン、カルタゴ')
                t = t.replace('コインブラ大学－アルタとソフィア', 'コインブラ大学')
                t = t.replace('コトルの自然と文化-歴史地域', 'コトルの(自然|文化|歴史地域)')
                t = t.replace('コースとセヴェンヌの地中海性農牧地の文化的景観', '(コース|セ(ヴェ|べ)ンヌ)の地中海性農牧地')
                # todo
                t = t.replace('ゴアの教会群と修道院群', 'ゴアの(教会群|修道院群)')
                t = t.replace('ゴブスタンのロック・アートと文化的景観', 'ゴブスタンのロック・アート')
                # todo
                # コロとその港
                t = t.replace('ゴール旧市街とその要塞群', 'ゴール(旧市街|要塞群)')
                t = t.replace('サルヤルカ-カザフスタン北部のステップと湖沼群', 'サルヤルカ-カザフスタン北部の(ステップ|湖沼群)')
                # todo
                t = t.replace('サンクト・ペテルブルグ歴史地区と関連建造物群', 'サンクト・ペテルブルグ')
                t = t.replace('シェーンブルン宮殿と庭園群', 'シェーンブルン')
                # todo
                t = t.replace('ジャムのミナレットと考古遺跡群', 'ジャムのミナレット')
                # todo
                t = t.replace('ストーンヘンジ、エーヴベリーと関連する遺跡', 'ストーンヘンジ|エーヴベリー')
                # todo
                t = t.replace('スホクラントとその周辺', 'スホクラント')
                t = t.replace('ゼレナー・ホラのネポムークの聖ヨハネ巡礼教会', 'ゼレナー・ホラ|ネポムーク')
                # todo
                t = t.replace('リミエ・モスクと複合施設群', 'リミエ・モスク')
                # todo
                t = t.replace('ソロヴェツキー諸島の文化と歴史遺産群', 'ソロ(ヴェ|ベ)ツキー諸島')
                # todo
                t = t.replace('ダラム城と大聖堂', 'ダラム城')
                t = t.replace('チャンパサック県の文化的景観にあるワット・プーと関連古代遺産群',
                              'チャンパサック、ワット・プー')
                t = t.replace('ディヴリーイの大モスクと病院', 'ディヴリーイ')
                # todo
                t = t.replace('デリーのクトゥブ・ミナールとその建造物群', 'クトゥブ・ミナール')
                t = t.replace('トスカナ地方のメディチ家の別荘と庭園群', 'メディチ家の(別荘|庭園)')
                t = t.replace('ナスカとパルパの地上絵','(ナスカ|パルパ)の地上絵')
                t = t.replace('ニューカレドニアのラグーン：リーフの多様性とその生態系', 'ニューカレドニアのラグーン')
                t = t.replace('ノヴゴロドの文化財とその周辺地区', 'ノ(ヴ|ブ)ゴロド')
                t = t.replace('バミューダ島の古都セント・ジョージと関連要塞群', 'バミューダ島')
                t = t.replace('バンスカー・シュティアヴニツァ歴史都市と近隣の工業建築物群', 'バンスカー・シュティア(ヴ|ブ)ニツァ')
                t = t.replace('バーミヤン渓谷の文化的景観と古代遺跡群', 'バーミヤン渓谷')
                t = t.replace('パレスチナ：オリーブとワインの地－エルサレム南部バティールの文化的景観',
                              'パレスチナ、エルサレム、バティール')
                t = t.replace('パンノンハルマのベネディクト会修道院とその自然環境', 'パンノンハルマ、ベネディクト会修道院')
                t = t.replace('フォンテーヌブローの宮殿と庭園', 'フォンテーヌブローの(宮殿|庭園)')
                t = t.replace('ブハラ歴史地区', 'ブハラ')
                t = t.replace('ブリッジタウン歴史地区とその要塞', 'ブリッジタウン')
                t = t.replace('ホローケーの古村落とその周辺地区', 'ホローケー')
                # todo
                # t = t.replace('ポツダムとベルリンの宮殿群と公園群,
                t = t.replace('ポントカサステ水路橋と水路', 'ポントカサステ')
                t = t.replace('マテーラの洞窟住居と岩窟教会公園', 'マテーラの(洞窟住居|岩窟教会公園)')
                # todo
                t = t.replace('マドリードのエル・エスコリアル修道院とその遺跡', 'エル・エスコリアル修道院')
                # todo
                t = t.replace('ミール地方の城と関連建物群', 'ミール地方の(城|関連建物群)')
                t = t.replace('モン-サン-ミシェルとその湾', 'モン-サン-ミシェル')
                t = t.replace('ラバト：近代都市と歴史的都市が共存する首都', 'ラバト')
                t = t.replace('リオデジャネイロ：山と海の間のカリオッカの景観', 'リオデジャネイロ|カリオッカ')
                t = t.replace('ルイス・バラガン邸と仕事場', 'ルイス・バラガン')
                t = t.replace('ルクセンブルク市：その古い街並みと要塞群', 'ルクセンブル(ク|グ)')
                t = t.replace('レユニオン島の火山峰、圏谷と岩壁群', 'レユニオン島')
                t = t.replace('レーティシュ鉄道アルブラ線・ベルニナ線と周辺の景観', 'レーティッ?シュ鉄道')
                t = t.replace('レーロース鉱山都市とその周辺', 'レーロース')
                # ヴァイマールは除外
                t = t.replace('ヴァイマールとデッサウのバウハウスとその関連遺産群','デッサウ、バウハウス')
                t = t.replace('古典主義の都ヴァイマール', '(ヴァ|ワ)イマール')
                t = t.replace('ヴェズレーの教会と丘', '(ヴェ|ベ)ズレー')
                t = t.replace('ヴェネツィアとその潟', '(ヴェ|ベ)ネ(ツィ|チ)ア、ベニス')
                t = t.replace('ヴェルサイユの宮殿と庭園', '(ヴェ|ベ)ルサイユの(宮殿|庭園)')
                t = t.replace('ヴュルツブルク司教館、その庭園群と広場', '(ヴュ|ビュ)ルツブル(ク|グ)')
                t = t.replace('北京と瀋陽の明・清朝の皇宮群', '故宮博物院、紫禁城、瀋陽故宮')
                t = t.replace('古代都市「タウリカのヘルソネソス」とそのホーラ',
                              'タウリ(カ|ケ)の(ケ|へ)ルソネソス、(ケ|へ)ルソネソス・タウリ(カ|ケ)')
                t = t.replace('古代都市スコタイと周辺の古代都市群', 'スコー?タイ')
                t = t.replace('古代都市テーベとその墓地遺跡', 'テーベ')
                t = t.replace('古代都市パレンケと国立公園', 'パレンケ')
                t = t.replace('古代高句麗王国の首都と古墳群', '高句麗')
                t = t.replace('古都京都の文化財（京都市、宇治市、大津市）', '古都京都の文化財')
                t = t.replace('国境防備の町エルヴァスとその要塞群', 'エル(ヴァ|バ)ス')
                t = t.replace('富士山－信仰の対象と芸術の源泉', '富士山')
                t = t.replace('富岡製糸場と絹産業遺産群', '富岡製糸場')
                t = t.replace('武陵源の自然景観と歴史地域', '武陵源')
                t = t.replace('水銀関連遺産：アルマデンとイドリア', 'アルマデン、イドリア')
                t = t.replace('南登封の文化財“天地之中”', '南登封、天地之中')
                t = t.replace('河港都市グリニッジ', 'グリニッジ')
                t = t.replace('洗礼の地〝ヨルダン川対岸のベタニア″（アル・マグタス）', 'ベタニア、アル・マグタス')
                t = t.replace('済州火山島と溶岩洞窟群', '済州火山島')
                # todo
                t = t.replace('琉球王国のグスク及び関連遺産群',
                              'グスク')
                t = t.replace('石見銀山遺跡とその文化的景観', '石見銀山')
                t = t.replace('紀伊山地の霊場と参詣道', '紀伊山地の霊場、紀伊山地の参詣道')
                t = t.replace('紅河ハニ棚田群の文化的景観', '紅河ハニ棚田')
                # todo
                t = t.replace('開城の歴史的建造物と遺跡', '開城の(歴史的建造物|遺跡)')
                t = t.replace('開平の望楼群と村落', '開平の(望楼群|村落)')
                # todo
                t = t.replace('黄龍の景観と歴史地域', '黄龍の(景観と歴史地域)')

                t = re.sub(r'^古代都市', '', t)
                t = re.sub(r'^古都', '', t)
                t = re.sub(r'^歴史的城塞都市', '', t)
                t = t.replace('国立公園', '(国立)?公園')
                t = t.replace('王立公園', '(王立)?公園')
                t = t.replace('・', '・?')
                t = t.replace('-', '[-・]?')
                t = t.replace('の', 'の?')

                # t = t.replace('と', '、')
                t = t.replace('及び', '、')
                t = re.sub(r'(\s)+', '、', t)
                t = re.sub(r'(　)+', '、', t)
                t = t.replace('／', '、')
                t = t.replace('（', '(')
                t = t.replace('）', ')?')
                t = t.replace('：', '、')

                t = t.replace('、、', '、')

                if '、' in t:
                    t = f'({t.replace("、","|")})'

                f.write(heritage.formal_name + '\n')
                f.write(t + '\n')

                heritage.regex = t
                heritage.save()


class Blog(models.Model):
    domain = models.URLField(verbose_name='ドメイン', unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    author_name = models.CharField(verbose_name='筆者名', max_length=255, blank=True, null=True)
    author_id = models.CharField(verbose_name='筆者ID', max_length=255, blank=True, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Article(models.Model):
    url = models.CharField(verbose_name='URL', max_length=2048, unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    text = models.TextField(verbose_name='本文', blank=True, null=True)
    word_count = models.IntegerField(verbose_name='字数', blank=True, default=0)
    image_count = models.IntegerField(verbose_name='画像数', blank=True, default=0)
    word_count_per_image = models.IntegerField(verbose_name='画像あたり字数', blank=True, default=0)
    heritage = models.ManyToManyField(Heritage, verbose_name="世界遺産", blank=True)
    blog = models.ForeignKey(Blog, verbose_name='ブログ', on_delete=models.SET_NULL, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    @classmethod
    def update_word_count_per_image_all(cls):

        articles = cls.objects.all()

        for article in articles:

            if article.image_count:
                article.word_count_per_image = article.word_count // article.image_count
                article.save()

    def update_heritage(self, heritages=None):

        print(f'update_heritage run. Article.pk: {self.pk} title: {self.title}')

        if heritages is None:
            heritages = Heritage.objects.all()

        self.heritage.clear()

        if self.text:

            for heritage in heritages:

                if re.search(heritage.regex, self.text):
                    self.heritage.add(heritage)
                    print(f'Article.heritage add. heritage: {heritage.formal_name}')

            self.save()

    @classmethod
    def update_heritage_all(cls):

        articles = cls.objects.all()
        heritages = Heritage.objects.all()

        for article in articles:

            # article.update_heritage(heritages=heritages)

            print(f'update_heritage run. Article.pk: {article.pk} title: {article.title}')

            article.heritage.clear()

            if article.text:

                for heritage in heritages:

                    if re.search(heritage.regex, article.text):
                        article.heritage.add(heritage)
                        print(f'Article.heritage add. heritage: {heritage.formal_name}')

                article.save()

    def scraping_content(self):

        print(f'scraping_content run. Article.pk: {self.pk} url: {self.url}')

        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            if soup.html.get('data-admin-domain') == '//blog.hatena.ne.jp':
                self.title = soup.find(class_='entry-title').text
                self.text = soup.find(class_='entry-content').text
                self.word_count = len(soup.find(class_='entry-content').text)
                self.image_count = len(soup.find(class_='entry-content').find_all('img'))
                if self.image_count:
                    self.word_count_per_image = self.word_count // self.image_count

                blog_domain = soup.html.get('data-blog-host')

                if blog_domain:

                    try:
                        blog = Blog.objects.get(domain=blog_domain)

                    except ObjectDoesNotExist:
                        blog = Blog()
                        blog.domain = blog_domain

                    blog.title = soup.html.get('data-blog-name')
                    blog.author_name = soup.html.get('data-blog-owner')
                    blog.author_id = blog.author_name
                    blog.save()

                    self.blog = blog
                    print(f'Blog is created or updated. pk: {blog.pk} title: {blog.title}')

                self.save()
                print(f'Article is updated. title: {self.title}')

                self.update_heritage()

        except AttributeError:
            print(f'BeautifulSoup: AttributeError')

    @classmethod
    def scraping_content_all(cls):

        articles = cls.objects.all()
        for article in articles:

            if article.title:
                if 0 < article.word_count < 1000:
                    continue

            sleep(0.5)
            article.scraping_content()

    @classmethod
    def scraping_url(cls):

        bing = Bing()
        urls = bing.get_urls(required_url_number=5000)

        for url in urls:

            article = Article()
            article.url = url

            try:
                article.save()
            except IntegrityError:
                pass

    @classmethod
    def scraping_uncollected_heritage(cls):

        print(f'scraping_uncollected_heritage run.')

        bing = Bing()
        heritages = Heritage.objects.filter(article__isnull=True)

        bing.keywords = ['世界遺産', '旅', heritages[random.randrange(len(heritages))].formal_name]

        print(f'bing.keywords: {bing.keywords}')

        urls = bing.get_urls(required_url_number=50)

        for url in urls:

            article = Article()
            article.url = url

            try:
                article.save()
                print(f'Article is created. url:{url}')

                article.scraping_content()

            except IntegrityError:
                print(f'Article is not created.IntegrityError. url: {url}')
