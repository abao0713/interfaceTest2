
import unittest
from parameterized import parameterized
from commonsrc import HTMLTestRunner


class Testadd(unittest.TestCase):
    @classmethod  # 这里的装饰器@classmethod必须有，标识为一个类方法
    def setUpClass(cls):
        """setUpClass为类的初始化方法，在整个类运行前执行只执行一次"""
        pass

    def setUp(self):
        """为测试方法的初始化，每个case运行前执行一次"""
        self.a = 20
        self.b = 10

    def tearDown(self):
        """清理函数，和setUp类似，每个case执行后执行一次"""
        pass

    @classmethod
    def tearDownClass(cls):
        """和setUpclass类似，在调用整个类测试方法完成后执行一次"""
        pass

    def test_add(self):
        """验证加法"""
        result = self.a + self.b
        self.assertEqual(result, 30)

    def test_sub(self):
        """验证减法"""
        result = self.a - self.b
        self.assertEqual(result, 10)

    @unittest.skip('skipping test')
    def test_err(self):
        """错误验证"""
        result = self.a + self.b
        self.assertEqual(result, 3)

    @parameterized.expand([
        ('测试pass', 30,),
        ('测试error', 20,),
        ('测试error', 10,),
    ])
    def test_para(self, case, p):
        """参数化"""
        self._testMethodDoc = case  #这里将_testMethodDoc属性赋值可以解决测试报告中a.png的问题
        result = self.a + self.b
        self.assertEqual(result, p)

if __name__ == "__main__":
    # suite = unittest.TestSuite()
    # suite.addTest(Testadd('test_add'))
    # suite.addTest(Testadd('test_sub'))
    # suite.addTests([Testadd('test_add'), Testadd('test_sub'), Testadd('test_err')])
    suite = unittest.makeSuite(Testadd)
    # suite = unittest.TestLoader().loadTestsFromTestCase(Testadd)
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    filename = 'D:\\myreport.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(fp, title=u'my unit test', description=u'This is a report test')
    runner.run(suite)