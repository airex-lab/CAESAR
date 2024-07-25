import pytest
import numpy as np
from src.config import BATCH_SIZE
from src.data.radar_synthetic import get_dataloader
from src.model.agglomerative import AgglomerativeClusterer

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

def test_agglomerative_init():
    agglomerative = AgglomerativeClusterer()
    assert hasattr(agglomerative, 'run')

def test_agglomerative_run(features_scaled):
    agglomerative = AgglomerativeClusterer()
    results = agglomerative.run(None, features_scaled)
    
    assert 'scores' in results
    assert isinstance(results['scores'], dict)
    assert 'Silhouette Score' in results['scores']
    assert 'Calinski-Harabasz Index' in results['scores']
    assert 'Davies-Bouldin Index' in results['scores']
    
    assert 'labels' in results
    assert isinstance(results['labels'], np.ndarray)
    assert len(results['labels']) == len(features_scaled)
    
    assert 'optimal_k' in results
    assert isinstance(results['optimal_k'], int)
    assert results['optimal_k'] > 0