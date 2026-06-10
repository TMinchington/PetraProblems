/*
*
* Add lines to measure distance
*/
//

macro "Install Bio-Formats Extensions" {
//    run("Bio-Formats Macro Extensions");

wait(1000);
//run("Bio-Formats Macro Extensions");

args = getArgument();
//args = "/Users/thomas.minchington/Documents/petraCodeCheck/";
//args = "C:/Users/thoma/Desktop/petraTest/";
//argsArr = split(args, ",");
//input = argsArr[0];
suffix = "tif";
input = args;

function processFolder(input){
	list = getFileList(input);
//	print(list[0]);
	

	for (i=0; i < list.length; i++){
//		print(list[i]);
		if(File.isDirectory(input + File.separator + list[i])){
			print("folder");}
//			processFolder(input + File.separator + list[i]);}
		if(endsWith(list[i],suffix)){
			print("booo");
			filePath = input + "/" + list[i];
			print(filePath);
			processFile(filePath, input, list[i]);
			}
	}
	}
	
	
function processFile(filePath, input, file){

outputFolder = input + File.separator + "data/lines";
outfile_path = outputFolder + "/" + file.replace(".tif", "-line.txt");

print(outfile_path);
//exit();
if (File.exists(outfile_path)){
	print("Skipping: "+ filePath);
}else{
//Ext.setId(filePath);
//Ext.getFormat(filePath, format);
//Ext.getSeriesCount(sC);
//print(sC);
//


run("Bio-Formats", "open=[" + filePath +"]color_mode=Composite");
print("Hello");
roiManager("reset");
setTool("line");
waitForUser("Draw line for the measurement");
roiManager("add");
roiManager("select", 0);
roiManager("rename", "Petra line");
Roi.getContainedPoints(xpoints, ypoints);
getPixelSize(unit, pixelWidth, pixelHeight);

outfile = File.open(outfile_path);
print(outfile, "x_pixel" + '\t'+ "ypixel" +  '\t' + "x_um" + '\t'+ "y_um" + "\n");
for (i=0; i < xpoints.length; i++){

//	print(xpoints[i] + "\t" + ypoints[i]); 
	print(outfile, xpoints[i] + '\t'+ ypoints[i] +  '\t' + xpoints[i]*pixelWidth + '\t'+ ypoints[i]*pixelWidth + "\n");}
File.close(outfile);
run("Close All");}}

//
//	
processFolder(input);
run("Quit")
}