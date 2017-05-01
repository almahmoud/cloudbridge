import azure_test.helpers as helpers
from azure_test.helpers import ProviderTestBase


class AzureVolumeServiceTestCase(ProviderTestBase):
    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_create_and_get(self):
        volume = self.provider.block_store.volumes.create(
            "MyVolume", 1, description='My volume')
        print("Create Volume - " + str(volume))
        self.assertTrue(
            volume.name == "MyVolume", "Volume name should be MyVolume")

        volume = self.provider.block_store.volumes.get(
            "/subscriptions/7904d702-e01c-4826-8519-f5a25c866a96/resourceGroups/cloudbridge-azure/providers'\
            '/Microsoft.Compute/disks/MyVolume")
        print("Get Volume  - " + str(volume))
        self.assertTrue(
            volume.name == "MyVolume", "Volume name should be MyVolume")

        volume.delete()

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_delete(self):
        volume = self.provider.block_store.volumes.create("MyVolume", 1)
        volume.refresh()
        print("Create Volume - " + str(volume))
        self.assertTrue(volume.name == "MyVolume",
                        "Volume name should be MyVolume")
        volume.delete()
        volume1_id = "/subscriptions/7904d702-e01c-4826-8519-f5a25c866a96" \
                     "/resourceGroups/cloudbridge-azure/providers" \
                     "/Microsoft.Compute/disks/MyVolume"
        volume1 = self.provider.block_store.volumes.get(volume1_id)
        self.assertTrue(
            volume1 is None, "Volume still exists")

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_attach(self):
        volume = self.provider.block_store.volumes.create(
            "MyVolume", 1, description='My volume')
        self.assertTrue(
            volume.name == "MyVolume", "Volume name should be MyVolume")
        volume.attach("/subscriptions/7904d702-e01c-4826-8519-f5a25c866a96"
                      "/resourceGroups/CloudBridge-Azure/providers"
                      "/Microsoft.Compute/virtualMachines/ubuntu-intro1")
        volume.delete()

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_dettach(self):
        volume = self.provider.block_store.volumes.create(
            "MyVolume", 1, description='My volume')
        self.assertTrue(
            volume.name == "MyVolume", "Volume name should be MyVolume")
        volume.detach()
        volume.delete()

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_create_snapshot(self):
        volume = self.provider.block_store.volumes.create(
            "MyVolume", 1, description='My volume')
        self.assertTrue(
            volume.name == "MyVolume", "Volume name should be MyVolume")
        with self.assertRaises(NotImplementedError):
            snapshot = volume.create_snapshot("MySnap")
            self.assertTrue(
                snapshot is not None, "Snapshot not created")

        volume.delete()

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_get_ifNotExist(self):
        volume_id = "/subscriptions/7904d702-e01c-4826-8519-f5a25c866a96" \
                    "/resourceGroups/cloudbridge-azure/providers" \
                    "/Microsoft.Compute/disks/MyVolume123"
        volume = self.provider.block_store.volumes.get(volume_id)
        self.assertTrue(
            volume is None, "Volume should not be available")

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_find(self):
        volumes = self.provider.block_store.volumes.find("Volume")
        self.assertTrue(
            len(volumes) == 2, "Volume should not be available")

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_find_ifNotExist(self):
        volumes = self.provider.block_store.volumes.find("Volume123")
        self.assertTrue(
            len(volumes) == 0, "Volume should not be available")

    @helpers.skipIfNoService(['block_store.volumes'])
    def test_azure_volume_list(self):
        volume_list = self.provider.block_store.volumes.list()
        print("Volume List - " + str(volume_list))
        self.assertEqual(
            len(volume_list), 2)