PATH = getDirectory("Choose a folder");

file_list = getFileList(PATH);
//print(file_list.length);
for (i=0; i < file_list.length; i++){
		print(file_list[i], i);
		file_to_open = file_list[i];
		if (endsWith(file_to_open, "ome.tiff")){
			full_path = PATH + "/" + file_to_open;
			run("Bio-Formats", "open=full_path color_mode=Composite");
			save(replace(full_path, "ome.tiff", ",tif"));
			close("*");
			}
}


