from typing import Type

import pytest
from celery import Celery

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture
def celery_setup_name() -> str:
    return CeleryTestSetup.name()


@pytest.fixture
def celery_setup_config(celery_worker_cluster_config: dict) -> dict:
    return CeleryTestSetup.config(
        celery_worker_cluster_config=celery_worker_cluster_config,
    )


@pytest.fixture
def celery_worker_app(celery_worker_config: dict, celery_setup_name: str) -> Celery:
    return CeleryTestSetup.create_worker_app(
        celery_worker_config=celery_worker_config,
        celery_setup_app_name=celery_setup_name,
    )


@pytest.fixture
def celery_setup_app(celery_setup_config: dict, celery_setup_name: str) -> Celery:
    return CeleryTestSetup.create_setup_app(
        celery_setup_config=celery_setup_config,
        celery_setup_app_name=celery_setup_name,
    )


@pytest.fixture
def celery_setup_cls() -> Type[CeleryTestSetup]:
    return CeleryTestSetup


@pytest.fixture
def celery_setup(
    celery_setup_cls: Type[CeleryTestSetup],
    celery_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
    celery_setup_app: Celery,
) -> CeleryTestSetup:
    setup = celery_setup_cls(
        worker_cluster=celery_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
        app=celery_setup_app,
    )
    setup.ready()
    return setup