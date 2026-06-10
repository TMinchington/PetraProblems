/*
*
* Convert czi images to tif
*/
//
macro "blabla"{
//run("Bio-Formats Macro Extensions");
args = getArgument();
//args = "C:/Users/petra.schaffer/Documents/cellpose test,czi";
setBatchMode("hide");
//args = "/Users/thomas.minchington/Documents/petraCodeCheck,czi";
argsArr = split(args, ",");
input = argsArr[0];
suffix = argsArr[1];
//
//input = "/Users/thomas.minchington/Documents/petraCodeCheck"
//suffix = "czi"
print(File.isDirectory(input));
print(input);
print(suffix);

//input = "/Users/thomas.minchington/Documents/petraCodeCheck";
//suffix = "czi";

print("Hello");
function processFolder(input){
	list = getFileList(input);
//	print(list[0]);
	for (i=0; i < list.length; i++){
		print(list[i]);
		if(File.isDirectory(input + File.separator + list[i])){
			print("bla");}
		if(endsWith(list[i],suffix)){
			print("booo");
			filePath = input +"/"+ list[i];
			print(filePath);
			processFile(filePath);
			}
	}
	}
	
	
function processFile(filePath){
	
	print("Yo");
//	filePath2 = "/Users/thomas.minchington/Documents/petraCodeCheck/M132_48_40x_DAPI_CAG-GFP_Satb2(568)_Ctip2(647).czi";
//	run("Bio-Formats", "open=filePath2 color_mode=Composite series_1");
//	outname = replace(filePath2, "."+suffix, "");
//	print(outname);
//	saveAs("TIF", outname+".tif");
	outname = replace(filePath, "."+suffix, "");
	if( File.exists(outname+".tif")){
		print("Skipped:" + outname);
	}else {

	print(filePath);
	print(File.exists(filePath));
	
	run("Bio-Formats", "open=&filePath color_mode=Composite series_1");
	//exit();
	print(outname);
	
	saveAs("TIF", outname+".tif");
	run("Close All");
	}
}
//
//	
processFolder(input);
run("Quit")}