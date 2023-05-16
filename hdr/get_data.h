#include <iostream>
#include <vector>
#include <fstream>
#include <bits/stdc++.h>

using namespace std;

vector<float> string_track_to_vector(const string &str_track) {
    string str_parameter;
    vector<float> track;

    for (char c: str_track) {
        if (c == ',') {
            track.push_back(stof(str_parameter));
            str_parameter = "";
        } else if (c == ' ')
            continue;
        else
            str_parameter += c;
    }

    track.push_back(stof(str_parameter));

    return track;
}


vector<vector<vector<float>>> get_data(const string &path, const int &amount_parameters_in_hit) {
    vector<vector<vector<float>>> tracks;
    int track_id = 0;

    // Open file and read it line by line
    ifstream file(path);
    for (string str_track; !file.eof(); getline(file, str_track)) {
        if (str_track.empty())
            continue;

        // Convert line from file to vector
        vector<float> track = string_track_to_vector(str_track);

        vector<float> temp;
        int amount_characteristics = 0;
        int j = 0;
        tracks.emplace_back();

        // Separate characteristics to different vectors for each hit
        while (j < track.capacity()) {
            if (amount_characteristics < amount_parameters_in_hit) {
                if (amount_characteristics != 0 && amount_characteristics < 5)
                    temp.push_back(track[j]);
                amount_characteristics++;
                j++;
            } else {
                tracks[track_id].push_back(temp);
                temp.clear();
                amount_characteristics = 0;
            }
        }
        if (j == track.capacity())
            tracks[track_id].push_back(temp);
        track_id++;
    }

    return tracks;
}