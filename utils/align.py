from typing_extensions import Literal
from dataclasses import  dataclass
import json
from typing import List, Optional, Tuple
from functools import lru_cache
from itertools import chain
import Levenshtein

@dataclass
class Opcode:
    optype : Literal["insert","delete", "replace", "equal"]
    hypo_start : int
    hypo_end : int
    ref_start : int
    ref_end : int

    def align(self, hypo, ref) -> List[Tuple[str, str]]:
        output_hypo, output_ref = hypo[self.hypo_start:self.hypo_end], ref[self.ref_start:self.ref_end]

        def make_list(output_hypo, output_ref):
            if "" == output_hypo:
                for r in output_ref:
                    yield "", r
            elif "" == output_ref:
                for h in output_hypo:
                    yield h, ""
            else:
                for h,r in zip(output_hypo, output_ref):
                    yield h, r

        return list(make_list(output_hypo, output_ref))

@dataclass
class Diff:
    hypo : str
    ref : str

    def __hash__(self) -> int:
        return hash( (self.hypo, self.ref) )

    @property
    @lru_cache(maxsize=1)
    def opcodes(self):
        return [ Opcode(*opc)  for opc in Levenshtein.opcodes(self.hypo,self.ref )]

    @property
    @lru_cache(maxsize=1)
    def aligns(self) -> List[Tuple[str, str]]:
        squzeed = chain( *(opc.align(self.hypo, self.ref) for opc in self.opcodes) )
        return list(squzeed)

    @classmethod
    def make_aligns_json(cls, aligns):
        return json.dumps({

            "alignment": [ 
                {
                    "ref":alg[1],
                    "hyp":alg[0]
                }
                for alg in aligns
            ]
        }, ensure_ascii=False, indent=4)

def main():
    aligns = Diff(
        "如果合同没有约定时间但是符合以下条件的就是有效的一订立合同时当事人双方都具有相应的民事行为能力二双方在订立合同时意思表示真实不存在欺诈胁迫等情形三合同的内容不违反法律行政法规强制性规定不违背公序良俗满足以下条件的协议是有效的一订立协议时当事人双方都具有相应的民事行为能力二双方在订立协议时意思表示真实不存在欺诈胁迫等情形三协议的内容不违反法律行政法规的强制性规定不违背公序良俗合同解除后担保责任不一定能够免除如果主合同尚未履行就解除则担保责任可以免除因为此时担保债权尚未发生所以不需要承担担保责任或者主合同是因侵权人的责任而解除的担保责任也可以免除如果是中标后中标人不签合同的则可以取消其其中标资格投标保证金不予退还然后由有关行政监督部门责令改正可以处中标项目金额百分之千分之五以上千分之十以下的罚款如果是招标人拒绝签订合同的中标人可以书面催告其签订合同如果其还拒绝的则由有关行政监督部门责令改正可以处中标项目金额千分之五以上千分之十以下的罚款符合以下条件的借款合同就是有效的一订立合同时当事人双方具有相应的民事行为能力二双方在订立合同时意思表示真实不存在欺诈胁迫等情形三合同的内容不违反法律行政法规的强制性规定不违背公序良俗父母离婚时子女无论是否成年都无权参与财产分割离婚时对于夫妻共同财产首先由离婚双方协商分割如果协商分割不成可以向法院起诉法院根据财产的具体情况按照照顾子女女方和无故作坊权益的原则判决对于夫妻共同财产原则上是均等分割根据生产生活的实际需要和财产的来源等情况具体处理时也可以有所差别夫妻以书面形式约定婚姻关系存续期间所得的财产以及婚前财产归各自所有共同所有或部分各自所有部分共同所有的离婚时应按约定处理双方对夫妻共同财产中的房屋价值及归属无法达成协议时人民法院按以下情形分别处理一双方君主让房屋所有权并且同意竞价取得的应当准许二一方主张房屋所有权的由评估机构按照市场价格对房屋作出评估取得房屋所有权的一方应当给予另一方相应的补偿在双方均不主张房屋所有权的根据当事人的申请拍卖变卖房屋就所得价款进行分割原则上夫妻一方婚前个人财产不因婚姻关系的延续而转化为夫妻共同财产但可以通过以下方式变成夫妻共同财产一赠与赠与是一种无偿转移财产的行为赠与的法律后果是财产所有权的转移赠与完成后不能把已经送出去的财产再要回来如果是房屋汽车的赠与应当办理登记手续二夫妻财产约定夫妻可以通过书面财产约定的方式约定婚前个人财产为夫妻共同财产财产约定可以在婚前也可以在婚后但在婚前约定的话双方的约定到结婚的时候才能生效如果约定之后双方后来没有结婚的这个约定不产生法律效力固定期限的劳动合同到期不续签是否有补偿要根据以下情形分析一如果单位不续签需要进行经济补偿啊如果员工不取钱又细分为两种情况一如果单位维持或者提高原来劳动条件员工仍然不需钱的则不进行经济补偿二如果单位降低原来的劳动条件员工不续签的话可以要求经济补偿经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿新员工入职单位应当自入职之日起一个月内与其订立书面劳动合同自用工之日起一个月内经用人单位书面通知后劳动者不与用人单位订立书面劳动合同的用人单位应当书面通知劳动者终止劳动关系无需向劳动者支付经济补偿但是应当依法向劳动者支付其实际工作时间的劳动报酬用人单位自用工之日起超过一个月不满一年未与劳动者订立书面劳动合同的应当依照劳动合同法第八十二条的规定向劳动者每月支付两倍的工资并与劳动者补定书面劳动合同劳动者不与用人单位订立书面劳动合同的用人单位应当书面通知劳动者终止劳动关系并依照劳动合同法第四十七条的规定支付经济补偿一劳动合同期限终止用人单位不续订应当向劳动者支付经济补偿用人单位维持或者提高劳动合同约定的条件续订劳动合同劳动者不同意续订的单位无需支付经济补偿金二因下列情形之一导致劳动合同终止的用人单位应当向劳动者支付经济补偿一用人单位被依法宣告破产的二用人单位被吊销营业执照责令关闭撤销或者用人单位决定提前解散的经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资的标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿劳动合同期满终止用人单位维持或者提高劳动合同约定条件续订劳动合同劳动者不同意续订的单位无需支付经济补偿金用人单位不确定应当向劳动者支付经济补偿经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资的标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿员工无故旷工单位按照规章制度辞退该员工的无需支付经济补偿用人单位以旷工为由解除劳动合同需要制度落地即企业管理规章制度需要依据法律程序制定并为员工知晓以此为群体劳动者旷工行为构成严重违反规章制度时用人单位可以解除劳动合同根据工伤保险条例及相关法律法规工伤认定遵循两条原则首先要符合三公标准及职工在工作时间工作场所因工作原因啊受到事故伤害的应当认定为工伤工伤保险实行无过错补偿原则其核心内容是无论工伤的引起事故因劳动者本人的过错用人单位的过错以及第三人的过错劳动者均应依法享受工伤保险待遇工伤员工受伤C因违规操作造成但符合上述工伤认定的原则公司应为其申请工伤认定保证保证员工合法的权益我国禁止招用童工但并非一概禁止未成年人参加劳动十六岁以上的未成年人与用人单位订立的劳动合同是合同有效的此外对于一些文艺体育和特种工艺经过有关部门批准所订立的劳动合同也是有效的认定应然单位与未成年人订立的劳动合同的效力应当从未成年人是否具有劳动者的法定资格分析我国相关的劳动法律法规规定劳动者的劳动权利能力和行为能力始于十六周岁及未满十六周岁的未成年人是不具备劳动权利能力和行为能力用人单位不得招用未满十六周岁的未成年人也不得与之签订劳动合同即使签订了劳动合同应也因为未满十六周岁的未成年人不具备劳动者的资格而无效除文艺体育特种工艺单位在严格履行审批手续的前提下可以招用未满十六周岁的未成年人其他单位均不可招用未满十六周岁的未成年人劳动争议调解是指企业与员工之间由于社会保险薪资福利待遇劳动关系等发生争议时由第三方例如专业性的人才机构争议调解中心等进行的和解性的咨询通过劳动争议调解达到法律咨询和解方式等的说明发生劳动争议当事人可以到下列调解组织申请调解一企业劳动争议调解委员会二依法设立的基层人民调解组织在在乡镇街道设立的具有劳动争议调解职能的组织员工集体罢工严重违反了用人单位规章制度的单位有权解除劳动合同且无需支付经济补偿劳动者维权应当采用法律规定的",
        "如果合同没有约定时间但是符合以下条件的就是有效的1订立合同时当事人双方都具有相应的民事行为能力2双方在订立合同时意思表示真实不存在欺诈胁迫等情形3合同的内容不违反法律行政法规的强制性规定不违背公序良俗满足以下条件的协议是有效的1订立协议时当事人双方都具有相应的民事行为能力2双方在订立协议时意思表示真实不存在欺诈胁迫等情形3协议的内容不违反法律行政法规的强制性规定不违背公序良俗合同解除后担保责任不一定能够免除如果主合同尚未履行就解除的则担保责任可以免除因为此时担保债权尚未发生所以不需要承担担保责任或者主合同是因债权人的责任而解除的担保责任也可以免除如果是中标后中标人不签合同的则可以取消其中标资格投标保证金不予退还然后由有关行政监督部门责令改正可以处中标项目金额5以上10以下的罚款如果是招标人拒绝签订合同的中标人可以书面催告其签订合同如果其还拒绝的则由有关行政监督部门责令改正可以处中标项目金额5以上10以下的罚款符合以下条件的借款合同就是有效的1订立合同时当事人双方都具有相应的民事行为能力2双方在订立合同时意思表示真实不存在欺诈胁迫等情形3合同的内容不违反法律行政法规的强制性规定不违背公序良俗父母离婚时子女无论是否成年都无权参与财产分割离婚时对于夫妻共同财产首先由离婚双方协商分割如果协商分割不成可以向法院起诉法院根据财产的具体情况按照照顾子女女方和无过错方权益的原则判决对于夫妻共同财产原则上是均等分割根据生产生活的实际需要和财产的来源等情况具体处理时也可以有所差别夫妻以书面形式约定婚姻关系存续期间所得的财产以及婚前财产归各自所有共同所有或部分各自所有部分共同所有的离婚时应按约定处理双方对夫妻共同财产中的房屋价值及归属无法达成协议时人民法院按以下情形分别处理一双方均主张房屋所有权并且同意竞价取得的应当准许二一方主张房屋所有权的由评估机构按市场价格对房屋作出评估取得房屋所有权的一方应当给予另一方相应的补偿三双方均不主张房屋所有权的根据当事人的申请拍卖变卖房屋就所得价款进行分割原则上夫妻一方婚前个人财产不因婚姻关系的延续而转化为夫妻共同财产但可以通过以下方式变成夫妻共同财产1赠与赠与是一种无偿转移财产的行为赠与的法律后果是财产所有权的转移赠与完成后不能把已经送出去的财产再要回来如果是房屋汽车的赠与应当办理登记手续2夫妻财产约定夫妻可以通过书面财产约定的方式约定婚前个人财产为夫妻共同财产财产约定可以在婚前也可以在婚后但在婚前约定的话双方的约定到结婚的时候才能生效如果约定之后双方后来没有结婚则约定不产生法律效力固定期限的劳动合同到期不续签是否有补偿要根据以下情形分析一如果单位不续签需要进行经济补偿二如果员工不续签又细分为两种情况1如果单位维持或者提高原来劳动条件员工仍然不续签的则不进行经济补偿2如果单位降低原来劳动条件员工不续签的话可以要求经济补偿经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资的标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿新员工入职单位应当自入职之日起一个月内与其订立书面劳动合同自用工之日起一个月内经用人单位书面通知后劳动者不与用人单位订立书面劳动合同的用人单位应当书面通知劳动者终止劳动关系无需向劳动者支付经济补偿但是应当依法向劳动者支付其实际工作时间的劳动报酬用人单位自用工之日起超过一个月不满一年未与劳动者订立书面劳动合同的应当依照劳动合同法第八十二条的规定向劳动者每月支付两倍的工资并与劳动者补订书面劳动合同劳动者不与用人单位订立书面劳动合同的用人单位应当书面通知劳动者终止劳动关系并依照劳动合同法第四十七条的规定支付经济补偿一劳动合同期满终止用人单位不续订应当向劳动者支付经济补偿用人单位维持或者提高劳动合同约定条件续订劳动合同劳动者不同意续订的单位无需支付经济补偿金二因下列情形之一导致劳动合同终止的用人单位应当向劳动者支付经济补偿1用人单位被依法宣告破产的2用人单位被吊销营业执照责令关闭撤销或者用人单位决定提前解散的经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资的标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿劳动合同期满终止用人单位维持或者提高劳动合同约定条件续订劳动合同劳动者不同意续订的单位无需支付经济补偿金用人单位不续订应当向劳动者支付经济补偿经济补偿按劳动者在本单位工作的年限每满一年支付一个月工资的标准向劳动者支付六个月以上不满一年的按一年计算不满六个月的向劳动者支付半个月工资的经济补偿员工无故旷工单位依照规章制度辞退该员工的无需支付经济补偿用人单位以旷工为由解除劳动合同需要制度落地即企业管理规章制度需要依据法律程序制定并为员工知晓以此为前提劳动者旷工行为构成严重违反规章制度时用人单位可以解除劳动合同根据工伤保险条例及相关法律法规工伤认定遵循两条原则首先要符合三工标准即职工在工作时间工作场所因工作原因而受到事故伤害的应当认定为工伤工伤保险实行无过错补偿原则其核心内容是无论工伤的引起是否因劳动者本人的过错用人单位的过错以及第三人的过错劳动者均应依法享受工伤保险待遇员工受伤虽因违规操作造成但符合上述工伤认定的原则公司应为其申请工伤认定保证员工合法的权益我国禁止招用童工但并非一概禁止未成年人参加劳动16岁以上的未成年人与用人单位签订的劳动合同是合法有效的此外对于一些文艺体育或特种工艺经过有关部门批准所签订的劳动合同也是有效的认定用人单位与未成年人签订的劳动合同的效力应当从未成年人是否具有劳动者的法定资格分析我国相关劳动法律法规规定劳动者的劳动权利能力和行为能力始于16周岁即未满16周岁的未成年人是不具备劳动权利能力和行为能力用人单位不得招用未满16周岁的未成年人也不得与之签订劳动合同即使签订了劳动合同也因为未满16周岁的未成年人不具备劳动者的资格而无效除文艺体育和特种工艺单位在严格履行审批手续的前提下可以招用未满16周岁的未成年人其他单位均不可招用未满16周岁的未成年人劳动争议调解是指在企业与员工之间由于社会保险薪资福利待遇劳动关系等发生争议时由第三方例如专业性的人才机构争议调解中心等进行的和解性咨询通过劳动争议调解达到法律咨询和解方式等的说明发生劳动争议当事人可以到下列调解组织申请调解一企业劳动争议调解委员会二依法设立的基层人民调解组织三在乡镇街道设立的具有劳动争议调解职能的组织员工集体罢工严重违反用人单位规章制度的单位有权解除劳动合同且无需支付经济补偿劳动者维权应当采用法律规定的"
    ).aligns
    aligns = Diff.make_aligns_json(aligns)
    print(aligns)


if __name__ == "__main__":
    main()