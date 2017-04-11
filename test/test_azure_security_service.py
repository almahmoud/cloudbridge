import json
import unittest
import uuid

from cloudbridge.cloud.interfaces import TestMockHelperMixin

from test.helpers import ProviderTestBase
import test.helpers as helpers


class AzureSecurityServiceTestCase(ProviderTestBase):
    def __init__(self, methodName, provider):
        super(AzureSecurityServiceTestCase, self).__init__(
            methodName=methodName, provider=provider)

    @helpers.skipIfNoService(['security.security_groups'])
    def test_azure_security_group_list(self):
        sgl = self.provider.security.security_groups.list()
        found_sg = [g.name for g in sgl]
        for group in sgl:
            print("List( " + "Name-" + group.name + "  Id-" + group.id + " Rules - " + " )")
        self.assertTrue(
            len(sgl) == 2,
            "Count should be 3")

    @helpers.skipIfNoService(['security.security_groups'])
    def test_azure_security_group_get_found(self):
        sgl = self.provider.security.security_groups.get("sg3")
        print("Get ( " + "Name - " + sgl.name + "  Id - " + sgl.id + " )")
        self.assertTrue(
            sgl.name == "sec_group3",
            "SG name should be sec_group2")

    @helpers.skipIfNoService(['security.security_groups'])
    def test_azure_security_group_get_not_found(self):
        sgl = self.provider.security.security_groups.get("sg4")
        print(str(sgl))
        self.assertTrue(
            sgl == None,
            "Security group does not exist. Should return None.")

    @helpers.skipIfNoService(['security.security_groups'])
    def test_azure_security_group_delete_IdExists(self):
        sg = self.provider.security.security_groups.delete("sg2")
        print("Delete - ")
        self.assertEqual(sg, True)

    @helpers.skipIfNoService(['security.security_groups'])
    def test_azure_security_group_delete_IdNotExist(self):
        sg = self.provider.security.security_groups.delete("sg5")
        self.assertEqual(sg, False)