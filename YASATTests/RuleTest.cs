using YASATEngine;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;

namespace YASATTests
{
    
    
    /// <summary>
    ///This is a test class for RuleTest and is intended
    ///to contain all RuleTest Unit Tests
    ///</summary>
    [TestClass()]
    public class RuleTest
    {

        private TestContext testContextInstance;

        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext
        {
            get
            {
                return testContextInstance;
            }
            set
            {
                testContextInstance = value;
            }
        }

        #region Additional test attributes
        // 
        //You can use the following additional attributes as you write your tests:
        //
        //Use ClassInitialize to run code before running the first test in the class
        //[ClassInitialize()]
        //public static void MyClassInitialize(TestContext testContext)
        //{
        //}
        //
        //Use ClassCleanup to run code after all tests in a class have run
        //[ClassCleanup()]
        //public static void MyClassCleanup()
        //{
        //}
        //
        //Use TestInitialize to run code before running each test
        //[TestInitialize()]
        //public void MyTestInitialize()
        //{
        //}
        //
        //Use TestCleanup to run code after each test has run
        //[TestCleanup()]
        //public void MyTestCleanup()
        //{
        //}
        //
        #endregion


        /// <summary>
        /// Test each rules file, checking how well it catches real issues
        [TestMethod()]
        public void SQLiRealIssues()
        {
            RuleManager ruleGetter = new RuleManager();
            List<Rule> rules = GetRulesFromFile(YASATEngine.Settings.Default.RulesDirectory + "\\" + Settings.Default.SQLi); 
            string fileToTest = TestContext.DataRow["RealIssuesFile"]; //Create a file with a SQLi problem in it.
            actual = target.FindIssues(fileToTest);
            Assert.AreEqual(expected, actual);
            Assert.Inconclusive("Verify the correctness of this test method.");
        }

        /// Test each rules file, checking how well it avoids false positives
        [TestMethod()]
        public void AvoidFalseTest()
        {
            /// fill in later
        }
    }
}
