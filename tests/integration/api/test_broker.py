from __future__ import annotations

import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_BROKER
from pytest_celery import CELERY_BROKER_CLUSTER
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_BROKER)])
class test_celery_test_broker:
    def test_app(self, broker: CeleryTestBroker):
        assert broker.app is None


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BROKER_CLUSTER)])
class test_celery_broker_cluster:
    def test_app(self, cluster: CeleryBrokerCluster):
        broker: CeleryTestBroker
        for broker in cluster:
            assert broker.app is None

    def test_config(self, cluster: CeleryBrokerCluster):
        expected_keys = {"urls", "host_urls"}
        assert set(cluster.config().keys()) == expected_keys
