# -*- encoding:utf-8 -*-

import ConfigParser,os

class Configer:
    def __init__(self, config_filename):
        self.config_path = config_filename
        self.configer = ConfigParser.ConfigParser()
        if os.path.exists(config_filename):
            self.configer.read(config_filename)
        else:
            raise Exception("Config File Is Not Exists!")

    def get_sections(self):
        return self.configer.sections()

    def get_keys(self, section):
        return self.configer.options(section)

    def get(self, section, key, kind):
        if kind == "int":
            return self.configer.getint(section, key)
        elif kind == "float":
            return self.configer.getfloat(section, key)
        else:
            return self.configer.get(section, key)

    def set(self, section, key, value):
        if section in self.get_sections():
            self.configer.set(section,key, value)
        else:
            self.configer.add_section(section)
            self.configer.set(section,key, value)
            self.configer.write(open(self.config_path,'w'))
    

if __name__ == "__main__":
    configer = ConfigParser.ConfigParser()
    configer.read("test.ini")
    print configer.sections()
    print configer.items("app1")
    print configer.options("app1")
    print configer.get("app1","name")
    # print configer.get("app1","name3")
    print configer.getint("app1","port")
    print configer.getfloat("app1","port")
    configer.add_section("app3")
    configer.set("app3","name","test3")
    configer.write(open("test.ini",'w'))


