import p_editor


class BaseEditor:
    def __init__(self):
        self.m_fileName = "第一份导表.xls"
        self.m_writePath = "../objs/"
        self.m_defineName = "Defines"
        self.m_objName = "Person"
        self.Init()

    def Init(self):
        self.m_rootPath = "../session/"
        self.m_objPath = "Sheet1"
        self.m_definePath = "Sheet2"

        self.m_editor = p_editor.Editor(self.m_rootPath, self.m_fileName, self.m_objPath)
        self.m_define = p_editor.Editor(self.m_rootPath, self.m_fileName, self.m_definePath)

    def WriteAllLoad(self):
        sText = self.GetLoad()
        self.WriteLoad(sText)

    def WriteAllDfeine(self):
        sText = self.GetDefine()
        self.WriteDefine(sText)

    def WriteAllObj(self):
        for iIndex in range(len(self.m_editor.m_objDataList)):
            index, sText = self.GetObjContent(iIndex + 2)
            self.WriteObj(index, sText)

    def WriteObj(self, iIndex, sText):
        with open(self.m_writePath + self.m_objName.lower() + str(iIndex) + ".cs", "w", encoding="utf-8") as f:
            f.writelines(sText)

    def WriteLoad(self, sText):
        with open(self.m_writePath + "load.cs", "w", encoding="utf-8") as f:
            f.writelines(sText)

    def WriteDefine(self, sText):
        with open(self.m_writePath + "define.cs", "w", encoding="utf-8") as f:
            f.writelines(sText)

    def GetObjContent(self, iIndex):
        pass

    def GetObjId(self, iIndex):
        return self.m_editor.GetAtr(iIndex + 2, "ID")

    def GetDefine(self):
        sText = """
using System.Collections;
using System.Collections.Generic;

public enum %s
{
""" % (self.m_defineName)
        for iIndex in range(len(self.m_define.m_sDefine)):
            sDefine = "\t" + self.m_define.m_sDefine[iIndex] + "=" + \
                      self.m_define.m_sDefineValue[iIndex] + ",//" + \
                      self.m_define.m_sDefineName[iIndex] + "\n"
            sText += sDefine
        sText += "\n}"
        return sText

    def GetLoad(self):
        sName = self.m_objName
        sContent = ""
        for iIndex in range(len(self.m_editor.m_objDataList)):
            index = self.GetObjId(iIndex)
            s = "\t\tthis." + sName.lower() + "Dict.Add(" + str(index) + ", new " + sName + str(index) + "());\n"
            sContent += s
        sText = """
using System.Collections;
using System.Collections.Generic;

public class %sFactory
{
    private Dictionary<int,Person> %sDict = new Dictionary<int, %s>();
    
    public %sFactory()
    {
%s
    }

    public %s Create%s(int %sId)
    {
        return this.%sDict[%sId].Clone();
    }
}
        """ % (sName, sName.lower(), sName, sName, sContent, sName, sName, sName.lower(), sName.lower(), sName.lower())
        return sText
