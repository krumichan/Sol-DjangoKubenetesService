from core.ssh.ssh_client_sample import SshClientSample
from django.shortcuts import render

from common import constants as CC
from common.share import Share

mapper_path = CC.APPLICATION_ROOTDIR + CC.path.sep + Share().generator_path(__file__, CC.APPLICATION_MAPPERDIR)


def ssh_command_execute_test(request):

    client = SshClientSample(
        server="10.0.0.154"
        , username="root"
        , password="classact!"
    )

    command = "sudo docker run -d --privileged --restart=unless-stopped --net=host -v " \
              "/etc/kubernetes:/etc/kubernetes " \
              "-v /var/run:/var/run rancher/rancher-agent:v2.4.11-rc3 --server https://10.0.0.154 --token " \
              "qx59tzhkkhcxqbh4zr2gwv9kzqksf46hfxrd2sjzfp45q96r52vp2s --ca-checksum " \
              "d4738f1d0dc1266d31103023790974ef316ad78f7df2d11bca3307b72b0e4ebd --worker "

    print(client.execute(command))

    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="developTest.html")
        , context={"model": "success"}
    )


def create_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/createCluster.html")
    )


def delete_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/deleteCluster.html")
    )


def snapshot_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/snapshotCluster.html")
    )


def restore_snapshot_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/restoreSnapshotCluster.html")
    )


def node_run_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/noderunCluster.html")
    )


def rotate_certificates_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/rotateCertificatesCluster.html")
    )


def save_as_rke_templates_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/saveAsRkeTemplatesCluster.html")
    )


def run_cis_scan_cluster_test(request):
    return render(
        request=request
        , template_name=Share().generator_path(filepath=__file__, file="clusterTest/runCisScanCluster.html")
    )
