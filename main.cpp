#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

const int num_sampling = 100;
const int num_x = 1000;
const int dim = 10;

void read_x(vector<vector<vector<double>>> &x_sets)
{
    ifstream fin;
    fin.open("../thesis_data/samplingX.txt", ios::in);
    double read_cache;
    string header;
    for (int i = 0; i < num_sampling; i++)
    {
        for (int j = 0; j < dim; j++)
            fin >> header;
        vector<vector<double>> x;
        for (int j = 0; j < num_x; j++)
        {
            fin >> header;
            vector<double> x_cache;
            for (int k = 0; k < dim; k++)
            {
                fin >> read_cache;
                x_cache.push_back(read_cache);
            }
            x.push_back(x_cache);
        }
        x_sets.push_back(x);
    }
    fin.close();
}

void read_rotation(vector<vector<double>> &matrix, string file_path, int dim)
{
    ifstream fin;
    cout << file_path << endl;
    fin.open(file_path, ios::in);
    if (!fin)
        perror("Error: Cannot open input file for reading");
    for (int i = 0; i < dim; i++)
    {
        vector<double> tmp;
        for (int j = 0; j < dim; j++)
        {
            double num;
            fin >> num;
            tmp.push_back(num);
        }
        matrix.push_back(tmp);
    }
}

void experiment(vector<vector<vector<double>>> &x_sets, int problem_id,
                int experiment_id = 0, double subtract_lim = 0.,
                double rotate_lim = 0., double scale_factor = 1.,
                bool isSubstract = false, bool isRotate = false,
                bool isScale = false, string matrix_path = "")
{
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
    auto problem = problem_factory.create(problem_id, 1, dim);
    vector<vector<double>> y_sets;
    vector<vector<double>> rotation_matrix;
    if (isRotate)
        read_rotation(rotation_matrix, matrix_path, 10);
    for (int i = 0; i < num_sampling; i++)
    {
        vector<double> y;
        for (size_t j = 0; j < num_x; j++)
        {
            vector<double> tempx(x_sets[i][j]);
            if (isSubstract)
            {
                vector<double> offset;
                for (int k = 0; k < dim; k++)
                    offset.push_back((rand() / double(RAND_MAX) * 200. - 100.) *
                                     subtract_lim / 100.);
                subtract(tempx, offset);
            }
            if (isRotate)
            {
                vector<double> cacheX(tempx);
                for (int m = 0; m < dim; m++)
                {
                    tempx.at(m) = 0;
                    for (int n = 0; n < dim; n++)
                    {
                        tempx.at(m) =
                            tempx.at(m) + cacheX.at(n) * rotation_matrix[m][n];
                    }
                }
            }
            if (isScale)
            {
                for (int k = 0; k < dim; k++)
                    tempx[k] = tempx[k] * scale_factor;
            }
            double res = (*problem)(tempx);
            y.push_back(res);
        }
        y_sets.push_back(y);
    }
    ofstream fout;
    stringstream ss;
    ss << "../thesis_data/rotation/" << to_string(problem_id) << "_"
       << to_string(experiment_id) << "_" << to_string(subtract_lim) << "_"
       << to_string(rotate_lim) << "_" << to_string(scale_factor) << "_"
       << to_string(isSubstract) << "_" << to_string(isRotate) << "_"
       << to_string(isScale) << ".txt";
    fout.open(ss.str(), ios::out);
    for (size_t i = 0; i < y_sets.size(); i++)
    {
        for (size_t j = 0; j < y_sets[i].size(); j++)
        {
            fout << y_sets[i][j] << " ";
        }
        fout << endl;
    }
    fout.close();
}


int main()
{
    CecUtils cec_utils;
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);

    // vector<double> factors;
    // int factor_size = 20;
    // for (int i = 0; i < factor_size; i++)
    //     factors.push_back((i + 1) * 100. / factor_size);

    vector<double> factors = {0.015625, 0.03125, 0.0625, 0.125, 0.25,
                              0.5,      1.,      2.,     4.,    8.,
                              16.,      32.,     64.,    128.};

    vector<string> matrix_path;
    for (int i = 0; i < 30; i++)
    {
        stringstream ss;
        ss << "../thesis_data/rotation_matrix/" << i << "_rotation_10.txt";
        matrix_path.push_back(ss.str());
    }

    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        experiment(x_sets, problem_id);
        for (int matrix_ind = 0; matrix_ind < matrix_path.size(); matrix_ind++)
        {
            experiment(x_sets, problem_id, 0, 0.0, matrix_ind, 1.0, false, true,
                       false, matrix_path[matrix_ind]);
        }
    }
}