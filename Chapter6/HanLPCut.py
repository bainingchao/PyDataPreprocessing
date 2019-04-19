#coding=utf8

"""
DESC: hanlp分词操作详解
Author：伏草惟存
Prompt: code in Python3 env
"""

'''
JPype is an effort to allow python programs full access to java class
libraries
pip install JPype1
>pip install wheel
>pip install JPype1-0.6.3-cp37-cp37m-win_amd64.whl
'''

from jpype import *

# 调用HanLP的java包，如下路径下载并解压c盘即可：
# 启动JVM，Linux需替换分号;为冒号:
startJVM(getDefaultJVMPath(), "-Djava.class.path=C:\hanlp\hanlp-1.3.2.jar;C:\hanlp", "-Xms1g", "-Xmx1g")


paraStr1='中国科学院计算技术研究所的宗成庆教授正在教授自然语言处理课程'

print("="*30+"HanLP分词"+"="*30)
HanLP = JClass('com.hankcs.hanlp.HanLP')
print(HanLP.segment(paraStr1))



print("="*30+"标准分词"+"="*30)
StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
print(StandardTokenizer.segment(paraStr1))



# NLP分词NLPTokenizer会执行全部命名实体识别和词性标注
print("="*30+"NLP分词"+"="*30)
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
print(NLPTokenizer.segment(paraStr1))



print("="*30+"索引分词"+"="*30)
IndexTokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
termList= IndexTokenizer.segment(paraStr1);
for term in termList :
  print(str(term) + " [" + str(term.offset) + ":" + str(term.offset + len(term.word)) + "]")



print("="*30+" 极速词典分词"+"="*30)
SpeedTokenizer = JClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')
print(NLPTokenizer.segment(paraStr1))



paraStr2 = '攻城狮逆袭单身狗，迎娶白富美，走上人生巅峰'
print("="*30+" 自定义分词"+"="*30)
CustomDictionary = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
CustomDictionary.add('攻城狮')
CustomDictionary.add('单身狗')
HanLP = JClass('com.hankcs.hanlp.HanLP')
print(HanLP.segment(paraStr2))



print("="*20+"命名实体识别与词性标注"+"="*30)
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
print(NLPTokenizer.segment(paraStr1))



paraStr3="水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标,有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批,严格地进行水资源论证和取水许可的批准。"
print("="*30+"关键词提取"+"="*30)
print(HanLP.extractKeyword(paraStr3, 8))

paraStr0 ="据报道，2017年5月，为了承接一项工程，来自河南一家建筑公司的柳先生和十几名同事被派到南京做前期筹备工作。为了节约开支，大伙商量决定采取A A制的方式搭伙做饭。不料，2017年11月建邺区市场监管局(下称市监局)上门进行检查，要求柳先生等人不得在出租房内做饭，并且开出了一份《行政处罚听证告知书》。《告知书》显示柳先生等人搭伙做饭属于“未经许可从事食品经营的行为”，并认定其违法收入为14160元，加上10倍的罚款，总共要处罚155760元。对此，柳先生等人表示很不能理解市监局的这一处罚。因协商无果，柳先生等人已就此提起申诉。而在此之后，市监局向媒体提供了一份建筑公司出具的情况说明，证明该建筑公司承认出租房为单位员工食堂。针对此事，很快热议如潮。甚至有网友感慨道：“原来自己吃饭也要办理《食品生产经营卫生许可证》！”在当下食品卫生问题备受关注的大环境下，此次执法行动非但没有因其严格而受到好评，反而受到民众的质疑，这着实令人深思。\
\
根据《餐饮服务食品安全操作规范》规定，食堂指设于机关、学校(含托幼机构)、企事业单位、建筑工地等地点(场所)，供应内部职工、学生等就餐的提供者。建邺区市监局就是根据这一规定认定柳先生等人的搭伙做饭属于开设食堂的。而作为食堂就应该遵守食品安全法第35条第1款规定，必须有食品经营许可证。《食品安全法》第35条第1款的确规定了，从事食品生产、食品销售、餐饮服务，应当依法取得许可。\
\
为了证明是食堂，案发后，建邺区市监局还向媒体提供了一份该建筑公司的“情况说明”。而被处罚方柳先生表示，“该情况说明和授权书都是在市监局的工作人员诱导下写的，当时他们承诺不罚款，我们才按照他们给的模板写的”，“单位一开始不愿意盖章，协商了好几天才盖了章”。那么真相到底是什么？到底是员工个人搭伙做饭，还是公司开办的简易食堂，双方各执一词。不过，认定是否开设食堂，不能仅以单位自我“说明”为依据，而应该依照事实做出判别。如果是单位食堂，必须由单位出钱购买一切厨房用具，以及食品原材料，安排有专门的厨师，还要有专门的经营管理者。单位不能仅仅是在找地方解决了员工吃饭问题这个意义上自认食堂。对此，柳先生还说：“比如说买100块钱的菜，我们5个人吃，就一人20块钱，烧菜的师傅是不赚一分钱的。因此，张师傅做的饭一没出售二没盈利，怎么就成了‘食品经营行为’？”\
\
与此同时，南京市别的几个区市监局工作人员则表示，柳先生等人搭伙做饭规模小，而且是在民宅内，不需要办理许可证，只要做到不扰民就行。也就是说，同在南京市的不同市监局的态度完全不同，那这究竟是理解上有偏差，还是执法上的随意扩张呢？实际上，食品安全法第36条还规定，食品生产加工小作坊和食品摊贩等从事食品生产经营活动，应当符合本法规定的与其生产经营规模、条件相适应的食品安全要求，保证所生产经营的食品卫生、无毒、无害，食品药品监督管理部门应当对其加强监督管理。这一条对“小作坊和食品摊贩”等从事食品生产经营活动只提出“与其生产经营规模、条件相适应的食品安全要求”，这也说明，不是只要有食品生产就必须去办个许可证，否则那些小摊小贩小作坊就根本没有存在的空间，可社会又实实在在需要它们。\
\
再就处罚而言，根据《食品安全法》规定，未取得食品生产经营许可从事食品生产经营活动，由县级以上人民政府食品药品监督管理部门没收违法所得和违法生产经营的食品以及用于违法生产经营的工具、设备、原料等物品；违法生产经营的食品货值金额不足一万元的，并处五万元以上十万元以下罚款；货值金额一万元以上的，并处货值金额十倍以上二十倍以下罚款。再次，法律强调的处罚依据是“食品货值”，“货值”与为分摊成本而进行的搭伙做的饭菜有明显区别，这种搭伙的“自给自足”行为在本质上仍然属于自己做饭自己吃，只不过吃饭的人比单独的一家人或几家人多。这样的执法就有管得太宽、管得太随意之嫌。就当是该管，也有高射炮打蚊子的嫌疑。\
\
媒体还报道了此次执法人员的蛮横无理：“不要跟我谈凑钱，你那白纸黑字的东西都在这里，我跟你讲有问题，你要跟我狡辩，我们之间免谈，不交按20倍处罚，我管你，我们就等你告我们。”这番滥用法律当“威胁”筹码的语调，让国家机关工作人员的公正执法形象荡然无存。这一事件再次验证了基层执法矛盾与部分执法人员执法水平低，且容易滥用执法权，因而选择性地实施作为或者不作为大有关系。\
\
作为食品药品安全卫生监督管理部门，市监局严格认真执法本无可厚非。但此次重罚搭伙吃饭的做法除了反映执法能力问题外，滥用执法权力的冲动亦不可忽视。每一个执法者都须切记，执法的核心宗旨是保护公民的合法权益，人民授予的权力更不可被滥用。"


print("="*30+"自动摘要"+"="*30)
print(HanLP.extractSummary(paraStr0, 5))



paraStr4=["武胜县新学乡政府大楼门前锣鼓喧天","蓝翔给宁夏固原市彭阳县红河镇黑牛沟村捐赠了挖掘机"]
print("="*30+"地名识别"+"="*30)
HanLP = JClass('com.hankcs.hanlp.HanLP')
segment = HanLP.newSegment().enablePlaceRecognize(True)
for sentence in paraStr4 :
  print(HanLP.segment(sentence))



paraStr5="徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"
print("="*30+"依存句法分析"+"="*30)
print(HanLP.parseDependency(paraStr5))




text =r"算法工程师\n 算法（Algorithm）是一系列解决问题的清晰指令，也就是说，能够对一定规范的输入，在有限时间内获得所要求的输出。如果一个算法有缺陷，或不适合于某个问题，执行这个算法将不会解决这个问题。不同的算法可能用不同的时间、空间或效率来完成同样的任务。一个算法的优劣可以用空间复杂度与时间复杂度来衡量。算法工程师就是利用算法处理事物的人。\n \n 1职位简介\n 算法工程师是一个非常高端的职位；\n 专业要求：计算机、电子、通信、数学等相关专业；\n 学历要求：本科及其以上的学历，大多数是硕士学历及其以上；\n 语言要求：英语要求是熟练，基本上能阅读国外专业书刊；\n 必须掌握计算机相关知识，熟练使用仿真工具MATLAB等，必须会一门编程语言。\n\n2研究方向\n 视频算法工程师、图像处理算法工程师、音频算法工程师 通信基带算法工程师\n \n 3目前国内外状况\n 目前国内从事算法研究的工程师不少，但是高级算法工程师却很少，是一个非常紧缺的专业工程师。算法工程师根据研究领域来分主要有音频/视频算法处理、图像技术方面的二维信息算法处理和通信物理层、雷达信号处理、生物医学信号处理等领域的一维信息算法处理。\n 在计算机音视频和图形图像技术等二维信息算法处理方面目前比较先进的视频处理算法：机器视觉成为此类算法研究的核心；另外还有2D转3D算法(2D-to-3D conversion)，去隔行算法(de-interlacing)，运动估计运动补偿算法(Motion estimation/Motion Compensation)，去噪算法(Noise Reduction)，缩放算法(scaling)，锐化处理算法(Sharpness)，超分辨率算法(Super Resolution),手势识别(gesture recognition),人脸识别(face recognition)。\n 在通信物理层等一维信息领域目前常用的算法：无线领域的RRM、RTT，传送领域的调制解调、信道均衡、信号检测、网络优化、信号分解等。\n 另外数据挖掘、互联网搜索算法也成为当今的热门方向。\n"
print("="*30+"短语提取"+"="*30)
print(HanLP.extractPhrase(text, 10))


shutdownJVM()