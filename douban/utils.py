#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Py2utils:
     def __init__(self):
        print('I\'m GrandPa')

     @staticmethod
     def getCoding(strInput):
            '''
            获取编码格式
            '''
            if isinstance(strInput, unicode):
                return "unicode"
            try:
                strInput.decode("utf8")
                return 'utf8'
            except:
                pass
            try:
                strInput.decode("gbk")
                return 'gbk'
            except:
                pass




     @staticmethod
     def tran2UTF8(strInput):
            '''
            转化为utf8格式
            '''
            strCodingFmt = Py2utils.getCoding(strInput)
            if strCodingFmt == "utf8":
                return strInput
            elif strCodingFmt == "unicode":
                return strInput.encode("utf8")
            elif strCodingFmt == "gbk":
                return strInput.decode("gbk").encode("utf8")

     @staticmethod
     def tran2GBK(strInput):
            '''
            转化为gbk格式
            '''
            strCodingFmt = Py2utils.getCoding(strInput)
            if strCodingFmt == "gbk":
                return strInput
            elif strCodingFmt == "unicode":
                return strInput.encode("gbk")
            elif strCodingFmt == "utf8":
                return strInput.decode("utf8").encode("gbk")

     @staticmethod
     def is_chinese(uchar):
            """判断一个unicode是否是汉字"""
            if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
            else:
                return False

     @staticmethod
     def is_number(uchar):
            '''判断一个unicode是否是数字'''
            if uchar >= u'\u0030' and uchar <= u'\u0039':
                return True
            else:
                return False

     @staticmethod
     def is_alphabet(uchar):
            '''判断一个unicode是否是英文字母'''
            if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
            else:
                return False



     @staticmethod
     def is_other(uchar):
            '''判断是否非汉字，数字和英文字符'''
            if not (Py2utils.is_chinese(uchar) or Py2utils.is_number(uchar) or Py2utils.is_alphabet(uchar)):
                return True
            else:
                return False

     @staticmethod
     def tran2GB18030(str):
         '''
         转化为GB18030格式
         '''
         if Py2utils.is_other(str):
             print "汉字,数字,英文:" + str

         return str.encode('GB18030')




     @staticmethod
     def B2Q(uchar):
            '''半角转全角'''
            inside_code = ord(uchar)
            if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
                return uchar
            if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code = 0x3000
            else:
                inside_code += 0xfee0
            return unichr(inside_code)

     @staticmethod
     def Q2B(uchar):
            '''全角转半角'''
            inside_code = ord(uchar)
            if inside_code == 0x3000:
                inside_code = 0x0020
            else:
                inside_code -= 0xfee0
            if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                return uchar
            return unichr(inside_code)

     @staticmethod
     def stringQ2B(ustring):
            '''把字符串全角转半角'''
            return "".join([Py2utils.Q2B(uchar) for uchar in ustring])

     @staticmethod
     def uniform(ustring):
            '''格式化字符串，完成全角转半角，大写转小写的工作'''
            return Py2utils.stringQ2B(ustring).lower()

     @staticmethod
     def string2List(ustring):
        '''将ustring按照中文，字母，数字分开'''
        retList = []
        utmp = []
        for uchar in ustring:
            if Py2utils.is_other(uchar):
                if len(utmp) == 0:
                    continue
                else:
                    retList.append("".join(utmp))
                utmp = []
            else:
                utmp.append(uchar)
            if len(utmp) != 0: retList.append("".join(utmp))
            return retList


if __name__ == "__main__":
            # test Q2B and B2Q
           # for i in range(0x0020, 0x007F):
                # print Q2B(B2Q(unichr(i))), B2Q(unichr(i))
                # test uniform
           # p= Py2utils()
            ustring = u'中国 人名ａ高频Ａ'
            print Py2utils.tran2GB2312(ustring)
            ustring =  Py2utils.uniform(ustring)
            print ustring
            ret = Py2utils.string2List(ustring)
            print ret
