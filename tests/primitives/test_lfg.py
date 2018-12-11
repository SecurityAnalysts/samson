from samson.prngs.lfg import LFG
import unittest


# Test vector manually generated using Go's Additive LFG.
# NOTE: Go must do some weird internal int64 math and comes up with numbers I wasn't able to reproduce.
# Notice, we skip the first number and only test 250 numbers instead of 1000.
# Reference code:

# package main

# import (
# 	"fmt"
# 	"math/rand"
# )

# func main() {
#     s2 := rand.NewSource(42)
#     r2 := rand.New(s2)
#     r2.Uint64()
#     for i := 0; i < 250; i++ {
#         fmt.Printf("%d, ", r2.Uint64());
#     }
# }


class LFGTestCase(unittest.TestCase):
    def test(self):
        feed = 0
        tap = 334
        state = [-204604804849473497, 4978660247881509547, 7815724132203751755, -1925831237928058062, -1981311040946414386, -7140159485058386757, -6123016579623331044, -7995689788223287924, 7322098695133591315, 2787122079326112408, 1839971287024973278, -1465251644838025873, 527832092453699788, -3268878381899512229, -1255947932907140519, 5214393252761917383, 7583068718227409249, -3173594952576496759, 1245490180406585679, -4738528016440758119, -8930746249734895326, 3164280773886937396, 4663565261362889260, -6972002470473532310, 905639821494766829, -7439125889359395778, -4384822465266552129, 4455164259723008512, -3230791136645190029, -2849642045827823992, 3412712313341265347, -1047913716506691216, -3465952664886306133, 6309429205281426200, 8358699920983350383, 8113767813491909572, 4932968049958798741, -5862296346432449464, -328443323435795001, -601974184904471835, -2801233566025474221, 823713756876340210, -7786980043126907181, -3882535285752217107, -4239574072251955298, -1638920026015551026, 7475651390861770571, 5528986280010045452, -7351470944620250376, -8600573953964896940, 2096855144365486944, 866192246906858280, 770656068107680919, -2275609345521118022, 3161757106244110413, -2286589746549225441, -476361587536012671, -7033604822030745366, -2747921504682526521, -7694598386623802867, 4324247180956790886, 8282323225176360427, -8086741904163458515, -890398742689181817, -8650957658803426727, -875088012412921929, -6024398687400489353, -3003413192646676469, 1166802354943763017, -6693307757636074233, 1323063507231073646, -1206870141323334539, -2864830444795042173, -3990844877617078912, -7393004750986757305, 8540156361145638807, 3535965358769565681, 2127973277573759651, -7021306788518901384, 7961263479163791217, -1599870565434199175, 2352768477499386938, 7794806212170507292, -1598381530247384348, 1128649454063897179, 1347950790171517360, 8799799933772386819, 5893311712950650819, -4744159518377814179, 8978889111995726351, 4946416085741332775, 5030747463594540228, -5257034511704727250, -5685524613614056836, 8217448344785317905, 8399019415599348263, 350927997719605731, -3664007764707252513, 8049321590664538547, -7971743359489959112, -2835106691842895965, -7976769220126712553, -2259554580185519728, -2766396207885548866, -5347819781079082144, -9208366710561810536, 5232405779865848470, -5428502473305567029, -1281122153980705597, 982534037794925283, -2823211634206833993, -3503230580419084839, 3235332184963606641, -5972343185240818646, -4797442835773989596, 4718214379848231962, -6320873533751894677, -7916873905629005156, 5180658203987163786, 4070167728318039592, 2586729850002137956, -8631944176943049084, 3571950456552503482, 1562127531299600440, 1602448300492577664, 3468922126532323189, 1315822976028226432, -5254926472150697619, -6977282208953987160, 9049821756893835601, -8656601813375788285, 1075959087276726722, -2398279244744939608, 9052467513470518734, -6226627950193600941, -8397921405721886706, -7944985629142064227, -8678494162225390949, -8845991378435639871, 8079712579332682794, 8239244115664915045, 6574659059447700546, -3162679863108244466, 2523819888847168928, 3096501894890847261, -2305680602246361351, -4557361182526683092, -6958744249684800373, 349873025075979912, -6129230994638490333, -866822427222592472, 4170691980427706851, 3001706687016841562, -439118662853757940, 7572689498148605957, -2381652704322572766, -2504004881557898126, -7388544715570809561, 647731417277169646, 4265596798202530857, 4050537521827927489, -1925722207938427652, -3655056993956334621, 5882206836772961630, 3443455011104109829, 5975233207190489146, -684673683985727111, -6827402077283298235, -1757200353235739139, -1871609406106345314, -1169020870359979374, -1517759890242206860, 5836584236044442238, 6963317984140402277, -684721928337927888, -3050412167001373851, -6187751535489211996, -2941233290637088080, -1041631586165485024, 1626137708982023414, 6174294962656343433, 130420916876439808, 5576566108014297223, 6436260517944183105, -6881040722272389283, 6282444582249019265, -8542983302631186574, 2650418989258681084, -8076966850044538185, 3408554454648760716, 6691315431064913212, -3069351422988625803, 3231064916171043827, 3911860846388851269, -6955949697137545693, -2465146120881942269, 2026145330164851500, 7753377821637619822, 3004115090050795641, -5141812723308142445, 4470360204088402931, 6341454661755501214, -8289628364991453017, 5610954569586628951, -1265540852851453976, -4237480482052655150, 9076010553183206654, -446719483930663747, -5249180128285624513, 1536879141525934192, 4424808457292672829, 2527295502175122508, -1254028603351560878, 5770019955602522425, 1454736709196953773, -8942424269569532150, -6421720570227983184, 652728144219789612, -1608888203645403121, 5948135325970198556, 300924619788167956, 2105703216207901569, 9215293876255507176, 2042408158936910682, 583281041254407723, -8140578692695415135, 5339770307243492668, -5661599157731082175, -3898870091879534176, 9132933745070261267, -1415939234315681018, -7224774643541540478, 8892415088478238183, 6601362185959160683, 3877005134816041977, 2622607645447211143, -8714600099208131422, 8642348484905217517, 5638721587768302758, 677691318190229286, -1314887752721512909, -9004772933623816842, 2448301762417949333, 500344565188309072, 382360533177701313, -7778342291776560649, -8809248368932673849, 671040993940428012, -8955358154101522241, -5071514587522106286, 7507616690062827660, 5414895220996327603, -4201600144052647898, 323428046881750322, -543018456420072875, -6289190617897907112, -3144141317201207217, -6769569959448912372, 7350354663384462725, 5990863285084177574, -2604818392968340091, -5884011401262814429, 7601154748289808589, -3179735998004144248, 1677687726562403497, 4379911760952510342, 8893902018602461589, -6310321656669229581, 1759958555044318885, -2439182430155662968, -3304169736143868253, 3484765519441631727, 8825947601237282714, 7765303820965892600, -4441001609234600452, -8960692152661705704, 838570815485486970, 7074448711366870493, 7938562253942249107, -5516430282064330608, -4620452410050290906, -5861682507957306210, -2139036688776781651, 8267185653461398706, -454406576707454667, -8366273223570312770, -5080328751954418523, -1517038000322285800, -6002461307435949894, -5009244407785689391, -2963581282054596667, 3433517555950600114, 8527692288482558217, -1026809469465914915, -9127123175084321672, 6825268720391837019, 8472202260365442090, -7259415130521311747, -1305759519742598501, 2266332505169667426, -6198293085269249928, 8815246100004802983, 279957429078078027, 6061825796315929489, -7760280916848231877, -7867467148158697079, -7829404999656649177, -331923761379697768, -4987561650824677275, -3150658307868498642, 7989785544943785447, 8382709085037766548, -3063383913563007004, -8970983469726080073, -5068240257867391734, 5014431715183748064, 770528457503882170, -2451867654312446487, 6853639525002624270, 4307502341263515806, -3871538222526314921, -3864579331370368720, -7204750594759092366, 2472472068191613017, -7737753338280328481, 856525812293452100, -8446309148075659141, 2912263862289182240, 6713654209430723633, -4075357872110524160, -4791180927305803349, -1788107665950712192, 8264414914175363828, -7051849183823734470, -5082233682192162571, 4172198913005215908, -6774845080706608240, 7081030057573743358, -6526376737570708032, 4693413533751785907, -5884389046388398187, -8921563651111006907, -5171658157217536483, -8832421546134305086, 1404922017194980073, -3112930617281559436, 3539238430735052029, -5164692167507378794, -5206340938608046446, 3006183824307186136, 8846016493086029119, -496140448453136827, 8916313007702183788, 4454438797780439291, -2575514318304314252, -2963202884734649960, -3145449519501008398, 7841194704690278624, -4363535669667149263, 182756231757463001, -7209330062632477081, -4937915123602103678, 8325797136163719663, -6505613040022155178, -2918607383628135186, -1016510059557108661, 1192234187013700931, 2269223162996079676, 1374629160329725597, -4334402381312479295, 4716198764898515109, -7487524474158253461, -467176748836242697, 6099387306221814913, 6478133389641815292, 1526278903679695843, -2739987977604513419, 7490188444371563661, -8877973363017840711, 6375998953376926599, -5668415254656662265, -4988250164711525959, -7446854535724407626, 2563854497372018855, -6860684733512136625, 641531747073433148, 8527387820989670438, 6668260988707504617, -3086210127963102023, 3530853843568675067, -2694474371585050952, -3707406091958328381, 7997682129645602401, 2816302077378831306, 8200739122734489044, -8551710191613889850, 4575234608288423278, -1899853384520179854, -6199882830065940672, 8799453482822324917, -7836874702302043554, 6430883546002809138, 7040905939612384242, -2757209521240521268, -8376046457059000020, 7772538023352803198, 368796100842024033, -182710284015411390, 2858590450576694880, 1492293994997522110, 8513730317529441756, 4140812525840962318, 3846369064800549714, -6136315887777780506, -4614931794306469436, 4420976185471130820, -836952423093802098, 6643224941922636446, 3382291579181401238, 3685007562930657555, -1067684526099212540, 7847869447808195563, 203572724069967541, 6304399289111314392, -1273787448749250434, -1934816825512161225, -2033801437451962884, 516304439991366477, -1917174612112826693, -4385903313617163114, -7219267140267946021, -2560398713910110033, -6750637862855271555, -5517578859349233211, 7162160996641315379, -7167295695119880423, -2964812341899847130, -7819571600092320250, 8873637856849611357, -1259765807663048888, 1984156201370044706, -2779115033248811003, 1061771992177423369, -4640454062318227804, 472199340531854479, 7800732440580369180, 6939661476564250297, -7965225614729910769, 1862554673540242768, -8382161417460193463, 5987475107506212769, -2293278843926946045, -7831582118891392682, 7322941337502469493, -7887836934963181101, -1666208080602415320, -7058945127024351504, 7915532506155867578, -8227647662860090395, 7113530248223804971, 3836974469754137367, -1723069700581333617, 6048280198407563191, -2844629921290551952, -909637400117742697, 3072328541307616462, 2138013015221989584, 8382917531917522350, -9196886547453130069, -587296657004883811, -5546233216335364304, 538922349281605662, -4750891456907211857, -2152080386968411951, -5013915426319498242, 3508148137943463509, 8698188137642409938, 618695957576882322, 5262619785569011761, 4115815722331280686, -8184061974362245123, 5167678412612535116, 453497968339538545, -7315841134943288182, -3419542908705007154, 2025559015622619682, 5129839793551014962, -2909997338808504246, 737613870711396510, -2788637527791249121, 2348119883256983501, -791315483304350692, -7565055086814592647, 2015292915928617669, 8528594093888459771, -3189604947073756014, -7855209505816636776, -3919819171420449220, -3475230003353298213, -2304872940574138551, -7901033249957574850, 3140044591014083712, 8573413589427682541, -6524169351583960812, 1171018583893361660, 165273673111215586, 2748727527407739735, -7758135349176024648, -8031757281620002649, 8272371916981057783, -5595266153022616854, 8464592942712296327, 5526309326064457522, -6100665946765634967, -1578029338817630401, 6716068378364125212, -7202155120983750631, -2282232915355286550, 529352476392398396, 1027385667512016566, -2341872229714693854, -2971085023010720825, 9160397096453860059, 8491167443580173905, 6326109394296656073, -5354173691785700366, -1110072819330503430, 8606748115184708657, -7725120132025451071, -5170837473265638174, 1681710700672366518, -2361752275800158747, 9115578345470231069, 1593303941413452113, -8377944729727169085, 8065956667628785125, 5511772528387539231, -2906477322732016018, 3901442817725158294, -3564948282915817134, -96224010939306324, 990701261505646764, 2998528974313225625, -8459064676928423608, 7284242461869236757, 6714488869589602045, 662497920838608390, 6829286412268558325, 98010554226915487, 1790187118131614928, 6328999980277210560, -5781306366576098563, -8015913117227399524, -6508711106004345148, 5292279201686967123, 3767866067802118533, 2680349374482246536, 7731296305318425972, -4944495571442822055, -8352747384175266309, 9214960260322263624, 2053470223125828005, 2283511652996955395, 3487898694641700859, -1079558403842283496, 7668169974291648345, -1341673492723423939, -3534314952715191457, 3796186349227798008, -578061956729693682, -2547426810356567853, 1061155337262993902, 7605320303779787393, 6173592565522998166, 8641063345377015714, -2846709537935129053, -2673663610580875208, -8739431304633028698, -6421763583820944301, 9028091371275406837, 8880038265537859793, -3848632562744424324, 9169481784270887120, -5894952718669976172, 3483981009605977433, 6200870124832170102, -8375119046605219530, 4798739032872625425, 3670952233029118695, -3390832370647872536, 9022283080155211562, 6669701955823021582, -7406454371079551072, 4989762285366585702, -2022858039338192098, -8465217486784401, 4312510806751888297, 4476150858887316857, -6546934507342735040, 2768824213283497541, 4585204382594331007, -3179319842216486372, -4743860219000703991, 6717193513832427358, 7359890004052590952, 1567704259223268391, 126905650120023733]
        
        lfg = LFG(state=state, tap=tap, feed=feed, length=len(state))
        expected_output = [9832119173398632219, 5571782338101878760, 1926012586526624009, 9627525982598323465, 3534334367214237261, 7497468244883513247, 12769259138917390016, 12756335378660268676, 15185141594316539992, 6784982874943501314, 11233528261463674849, 12559306703000990798, 1118224062840270781, 15347792043893516350, 13523341480825645852, 6570415425842765075, 15826440160565561250, 8685383948212866759, 18177242848714785307, 1100641557378252013, 3137486211269163098, 11866690094643743981, 2094832826273809275, 6018823476402388478, 9610549860140450017, 8548114504158162025, 1198686371618757660, 4157513341729910236, 1947031852228291041, 3388162185735054281, 15879991964852500590, 17456309445381818697, 18422043553963299854, 9871652808949454819, 18202139891229947017, 8639902132831672016, 7894140303635748408, 10621455069619635027, 5785305945910038487, 16078261111520212762, 16195862262774206562, 2353959152108316618, 524317412587104192, 15721011318920817620, 14497752989399429727, 7697922259999977824, 5013667937579866784, 5135975278696416791, 7276889728610971305, 10947535027943645242, 1628829379025336882, 17877340767439212529, 7317580557654915562, 4914400674417821484, 2157255887366150544, 13403448691644081053, 2628757933617101898, 9584062475274761399, 2388284803033957873, 8427801741804500990, 15540436470826884759, 10769007981310868484, 6683509660637259755, 559346544157562657, 2750659816549965649, 12040198406101015711, 5328953735686644455, 8281354578677668636, 17217954477539939095, 2332036530383394983, 15667111415918593714, 4184787942719568102, 17435229622154663638, 15106441630554408643, 4988602387584303978, 13358884814933005762, 10131765283242706225, 4432433323786193433, 8063729658764635782, 17660099301260798508, 8890970237871203352, 11741004615292983676, 15998784133643001565, 4088882508931753773, 6520300896597308550, 16775912837935285774, 10664881372288894333, 11197754258325389363, 16546871691531966379, 11744933517914110057, 9164370140782074545, 7863941801268104373, 11031190374222403740, 6204000644254686808, 14103314530480599085, 3047082331882600663, 18004515891482477977, 13037594437536760110, 14565613859349568945, 9350089713366900418, 9057688761589453769, 12392988014061372798, 10506635487809909786, 17706347334497943808, 17687918572844101152, 4884111666020894591, 3034897366669354117, 6830935377660838268, 15110205943543510119, 12633942726829825522, 6025688929181751162, 10634297310096361340, 2316217535716785625, 16829824312865157525, 16046540386759797803, 3000848027476773113, 9236385975690319311, 10241933674851415976, 16991483444098001143, 10899859749153537387, 771530412271058804, 17554496667179666970, 15555711396058936263, 1990377109865472737, 18365242358036462219, 9815962615416642746, 13191826275514487340, 1025139303516356611, 17799899178434979962, 14309142707229038889, 13665263846661562108, 1327539235436002972, 2318279817119990980, 8554039893494197314, 3543037439332401303, 2207144605302255518, 1438848673159967689, 6784711405374479278, 1426967834779976657, 6049873861610840853, 6303393457478660289, 14467755250603183116, 3846685509774361260, 9456834653056323907, 8646707523083679814, 6487393459012818451, 17017291019302170013, 16501540993098480486, 1034491783883478295, 17824059464629383217, 3910358027411881903, 10689328055622810323, 13497236300158812926, 12241299663800182348, 15111833643617120547, 3046241816869124689, 3876831120760146157, 17258886580248420533, 9796796530641712959, 13902979460704652574, 13637316676624811418, 17401183523999199235, 12637269141031344438, 17636906659780629671, 13910428687225001474, 13603498197796298087, 16502304582060775617, 14848871064040100503, 14070627484721341195, 2917394494873114500, 7624391384633336572, 5236438788702887727, 16979702736188245894, 15961703009056810918, 16534076777076611229, 3838932217870796034, 11556835878534490376, 14147916757274152157, 8088993938139972434, 15973823973403830792, 1066889861504680337, 2896904531678456417, 5437576861888721920, 12521085803141028824, 8197742472884175475, 10420315297925538703, 17574390454113526079, 1076610976935039887, 9739726836813483707, 1686867465753366830, 1258296322362886354, 1959727265141231110, 2102928227887134539, 11926081644133232508, 13741565221114874063, 18281980229013602423, 11994052439565009499, 12907413118564359790, 12037405839500539285, 9421263614312542767, 5374258778607863590, 11146656703927278318, 7032932739093242063, 16090727696506219843, 17900345410758373594, 5354942899256810443, 10115276458850551349, 15715783370175934133, 18149338989681949426, 6137362139588023718, 13466984338648165248, 18015539019500991576, 5403031927380969262, 12067849857963641993, 1473252112028835405, 7835395796495495508, 15656724383526332006, 1632004251885129939, 1870818152933515021, 2555044635748851792, 3876863932037039789, 8082828759778330152, 18187386936874736478, 11982423575780069273, 12177371755017320060, 7349826345747322322, 11608404733242775069, 360404000129900369, 2142368663292481517, 12940359888219489331, 17713468397203727731, 16948108243224654355, 3264280614378918948, 10007823965383349807, 561797116506285086, 1052191000191262596, 14463269690116678052, 9773648575929073860, 10486671507781397581, 13953453647109195711, 12173199502447715705, 2112140079966405042, 16887547119428729213, 17304686248159446014, 8764669431729633759, 17130725724027725354, 8982556165529849820, 15431159194213919713, 8969844158754175803, 13702913023961158870]

        self.assertEqual([lfg.generate() for _ in range(251)][1:], expected_output)