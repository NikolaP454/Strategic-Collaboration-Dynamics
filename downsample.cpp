#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>

std::set<int> visited;

struct Edge {
    int author1;
    int author2;
    float power;
};

class Graph {
public:
    std::unordered_map<int, std::vector<std::pair<int, float>>> adjacencyList;

    Graph(const std::vector<Edge>& edges) {
        for (const auto& edge : edges) {
            adjacencyList[edge.author1].push_back({edge.author2, edge.power});
            adjacencyList[edge.author2].push_back({edge.author1, edge.power});
        }

        std::cout << "Graph created";
    }

    const std::unordered_map<int, std::vector<std::pair<int, float>>>& getAdjacencyList() const {
        return adjacencyList;
    }

    std::set<int> getAllAuthors() const {
        std::set<int> authors;
        for (const auto& [author, _] : adjacencyList) {
            authors.insert(author);
        }
        return authors;
    }

    void dfs(int author) const {
        if (visited.find(author) != visited.end()) {
            return;
        }

        visited.insert(author);

        for (const auto& [neighbor, power] : adjacencyList.at(author)) {
            if (visited.find(neighbor) == visited.end()) {
                visited.insert(neighbor);
                dfs(neighbor);
            }
        }
    }
};

// Function to read edges from a CSV file
std::vector<Edge> readEdgesFromCSV(const std::string& filename) {
    std::vector<Edge> edges;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file " << filename << std::endl;
        return edges;
    }

    std::string line;
    int counter = 0;
    while (std::getline(file, line)) {
        std::istringstream stream(line);
        int author1, author2;
        float power;

        // Read fields separated by spaces
        if (stream >> author1 >> author2 >> power) {
            edges.push_back({author1, author2, power});
            counter++;
        } else {
            std::cerr << "Error: Malformed line: " << line << std::endl;
        }

        int total_lines = 34000000;
        if (counter % 340000 == 0) {
            std::cout << "Read " << counter << " lines" << std::endl;
            std::cout << "Percentage (Estimate): " << (float)counter / total_lines * 100 << "%" << std::endl;
        }
    }

    file.close();
    return edges;
}

// Main function to test the Graph class
int main() {
    const std::string filename = "data/coauth-MAG-gr3.txt";
    const int DOWNSAMPLE_SIZE = 100000; // Example size
    const float THRESHOLD = 0;    // Example threshold

    std::vector<Edge> edges = readEdgesFromCSV(filename);
    Graph graph(edges);

    for (int author : graph.getAllAuthors()) {
        if (visited.size() >= DOWNSAMPLE_SIZE) {
            break;
        }

        if (visited.find(author) != visited.end()) {
            continue;
        }

        graph.dfs(author);
        
        std::cout << "Visited authors: " << visited.size() << std::endl;
    }

    std::cout << "Visited authors: " << visited.size() << std::endl;

    // Save visited authors to a new file
    std::ofstream authors_file("data/coauth-MAG-gr3-downsampled-authors.txt");
    for (int author : visited) {
        authors_file << author << std::endl;
    }
    authors_file.close();

    std::vector<Edge> downsampledEdges;

    for (const auto& [author, neighbors] : graph.getAdjacencyList()) {
        if (visited.find(author) == visited.end()) {
            continue;
        }

        for (const auto& [neighbor, power] : neighbors) {
            if (visited.find(neighbor) != visited.end()) {
                downsampledEdges.push_back({author, neighbor, power});
            }
        }
    }

    std::cout << "Downsampled edges: " << downsampledEdges.size() << std::endl;
    system("pause");

    // Save to a new file
    std::ofstream file("data/coauth-MAG-gr3-downsampled.txt");
    for (const auto& edge : downsampledEdges) {
        file << edge.author1 << " " << edge.author2 << " " << edge.power << std::endl;
    }
    file.close();

    return 0;
}
