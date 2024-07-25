from typing import Dict, Any
import matplotlib.pyplot as plt

from src.config import (
    np, AgglomerativeClustering, silhouette_score, MAX_CLUSTERS
)
from src.utils.scores import calculate_clustering_scores
class AgglomerativeClusterer:

    def run(self, _, features_scaled: np.ndarray) -> Dict[str, Any]:
        max_clusters = min(MAX_CLUSTERS, int(np.sqrt(len(features_scaled))))

        silhouette_scores = []
        for n_clusters in range(2, max_clusters + 1):
            agg_clustering = AgglomerativeClustering(n_clusters=n_clusters)
            labels = agg_clustering.fit_predict(features_scaled)
            silhouette_scores.append(silhouette_score(features_scaled, labels))

        optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2

        agg_clustering = AgglomerativeClustering(n_clusters=optimal_k)
        labels = agg_clustering.fit_predict(features_scaled)

        scores = calculate_clustering_scores(features_scaled, labels)

        return {
            'scores': scores,
            'labels': labels,
            'optimal_k': optimal_k
        }