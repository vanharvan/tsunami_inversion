clc; clear;

runFolder = fullfile(pwd, 'comcot_run');
outputFile = fullfile(pwd, 'run_list.txt');

% list all subdirectories in the run folder
items = dir(runFolder);
subDirs = items([items.isdir] & ~ismember({items.name}, {'.', '..'}));

% write file
fid = fopen(outputFile, 'w');

for i = 1:length(subDirs)
    fprintf(fid, '%s\n', subDirs(i).name);
end

fclose(fid);

fprintf('Found %d scenarios. Saved to %s\n', length(subDirs), outputFile);
