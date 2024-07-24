import pytest
import numpy as np
from src.config import BATCH_SIZE
from src.data.radar_synthetic import get_dataloader
from src.model.optics import OPTICSClusterer

@pytest.fixture
def dataloader():
    return get_dataloader(batch_size=BATCH_SIZE, shuffle=True)

@pytest.fixture
def features_scaled(dataloader):
    all_data = []
    for batch in dataloader:
        all_data.append(batch)
    all_data = np.concatenate(all_data, axis=0)
    return all_data

def test_optics_init():
    optics = OPTICSClusterer()
    assert hasattr(optics, 'run')

def test_optics_run(features_scaled):
    optics = OPTICSClusterer()
    results = optics.run(None, features_scaled)
    
    assert 'scores' in results
    assert isinstance(results['scores'], dict)
    assert 'Silhouette Score' in results['scores']
    assert 'Calinski-Harabasz Index' in results['scores']
    assert 'Davies-Bouldin Index' in results['scores']
    
    assert 'labels' in results
    assert isinstance(results['labels'], np.ndarray)
    assert len(results['labels']) == len(features_scaled)
    
    assert 'cluster_densities' in results
    assert isinstance(results['cluster_densities'], dict)
    
    assert 'parameters' in results
    assert isinstance(results['parameters'], dict)
    assert 'min_samples' in results['parameters']
    assert 'xi' in results['parameters']
    assert 'min_cluster_size' in results['parameters']