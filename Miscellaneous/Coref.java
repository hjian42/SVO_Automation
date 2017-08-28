import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.io.Writer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.coref.data.CorefChain.CorefMention;
import edu.stanford.nlp.coref.data.Dictionaries;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class Coref {
	static String[] pronouns = new String[] { "he", "she", "his", "him", "her", "they", "their" };
	static Map<String, String> decoder = new HashMap<String, String>();
	static Map<String, String> charsToReplace = new HashMap<String, String>();
	
	public static void decodeSpecialCharacters() {
		decoder.put("-LRB-", "(");
		decoder.put("-RRB-", ")");
		decoder.put("-LSB-", "[");
		decoder.put("-RSB-", "]");
	}
	
	public static void main(String[] args) throws Exception {
		Coref ce = new Coref();
		
		String inputDirectory = "";
		String outputDirectory = "";
		String inputFile = "";
		for (int i = 0; i < args.length; i++) {
            if ("-inputDir".equals(args[i])) {
            	inputDirectory = args[i + 1];
                i++;
            } else if ("-inputFile".equals(args[i])) {
                inputFile = args[i + 1];
                i++;
            } else if ("-outputDir".equals(args[i])) {
            	outputDirectory = args[i + 1];
                i++;
            }
        }
		
		decodeSpecialCharacters();
		fillCharsToReplace();
		//Annotation doc = new Annotation(content);
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		String outputFile;
		//getRepresentativeMentions("C:\\Users\\Doris\\Documents\\PC-ACE\\test\\corefex.txt", pipeline);
		//System.out.println(ce.replaceMentions("C:\\Users\\Doris\\Documents\\PC-ACE\\test\\corefex.txt", pipeline));
		
		if (inputFile.length() > 0) {
			//check file extension
			String extension = "";

			int i = inputFile.lastIndexOf('.');
			if (i > 0) {
			    extension = inputFile.substring(i+1);
			}
			
			//if not txt, exit method
			if (!extension.equals("txt")) {
				System.out.println("ERROR: Invalid file type; " + inputFile + " is not a txt file. Please use a txt file.");
				return;
			}
			
			//read in/output one file
			File input = new File(inputFile);
			if (outputDirectory.length() > 0  && outputDirectory.charAt(outputDirectory.length()-1) == File.separatorChar) {
				//outputDirectory ends in \
				outputFile = outputDirectory + input.getName().replaceFirst("[.][^.]+$", "") + "-out";
			} else if (outputDirectory.length() > 0  && outputDirectory.charAt(outputDirectory.length()-1) == '"') {
				//outputDirectory ends in " due to read-in error
				outputDirectory = outputDirectory.substring(0, outputDirectory.length()-1);
				outputFile = outputDirectory + File.separator + input.getName().replaceFirst("[.][^.]+$", "") + "-out";
			} else if (outputDirectory.length() > 0) {
				//outputDirectory does not end in \, must add to outputFile
				outputFile = outputDirectory + File.separator + input.getName().replaceFirst("[.][^.]+$", "") + "-out";
			} else {
				outputFile = input.getName().replaceFirst("[.][^.]+$", "") + "-out";
			}
			
			Writer writer = new OutputStreamWriter(new FileOutputStream(outputFile + ".txt"), "UTF-8");
			
			String resolved = ce.replaceMentions(inputFile, pipeline);
			
			writer.write(resolved);
			
			writer.close();
		} else if (inputDirectory.length() > 0) {
			if (inputDirectory.charAt(inputDirectory.length()-1) == '"') {
				inputDirectory = inputDirectory.substring(0, inputDirectory.length()-1);
			}
			System.out.println(inputDirectory);
			//read in/output all files in a folder
			File dir = new File(inputDirectory);
			File[] directoryListing = dir.listFiles();
			
			if (directoryListing != null) {
				for (File child : directoryListing) {
					inputFile = child.getAbsolutePath();
					System.out.println(inputFile);

					//check file extension
					String extension = "";

					int i = inputFile.lastIndexOf('.');
					if (i > 0) {
					    extension = inputFile.substring(i+1);
					}
					
					//if not txt, skip file
					if (!extension.equals("txt")) {
						System.out.println("ERROR: Not a txt file. " + inputFile + " skipped.");
						continue;
					}
					
					//replaceSpecialCharacters(inputFile);
					if (outputDirectory.length() > 0 && outputDirectory.charAt(outputDirectory.length()-1) == File.separatorChar) {
						//outputDirectory already ends in \
						outputFile = outputDirectory + child.getName().replaceFirst("[.][^.]+$", "") + "-out";
					} else if (outputDirectory.length() > 0 && outputDirectory.charAt(outputDirectory.length()-1) == '"') {
						//outputDirectory ends in " due to read-in error
						outputDirectory = outputDirectory.substring(0, outputDirectory.length()-1);
						outputFile = outputDirectory + File.separator + child.getName().replaceFirst("[.][^.]+$", "") + "-out";
					} else if (outputDirectory.length() > 0) {
						//outputDirectory does not end in \, must add to outputFile
						outputFile = outputDirectory + File.separator + child.getName().replaceFirst("[.][^.]+$", "") + "-out";
					} else {
						outputFile = child.getName().replaceFirst("[.][^.]+$", "") + "-out";
					}
					Writer writer = new OutputStreamWriter(new FileOutputStream(outputFile + ".txt"), "UTF-8");
					
					String resolved = ce.replaceMentions(inputFile, pipeline);
					
					writer.write(resolved);
					
					writer.close();
				}
			} else {
			    //dir is not really a directory
				System.out.println("invalid directory");
			}
		} else {
			System.out.println("Please put an input directory.");
		}
		
		  
		//ce.checkForUnresolvedPronouns(resolved);
	}
	
	/**
	 * Attempts to resolve coreferences to animate objects in the given file.
	 * @param filename - text file to read and edit content of
	 * @return String with resolved coreferences
	 * @throws IOException 
	 */
	public String replaceMentions(String filename, StanfordCoreNLP pipeline) throws IOException {
		String content = readFile(filename);
		Annotation doc = new Annotation(content);
		pipeline.annotate(doc);

		Map<Integer, CorefChain> corefs = doc.get(CorefChainAnnotation.class);
		List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);

		List<String> resolved = new ArrayList<String>();

		for (CoreMap sentence : sentences) {
			//System.out.println(sentence);
			List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

			for (CoreLabel token : tokens) {

				Integer corefClustId = token.get(CorefCoreAnnotations.CorefClusterIdAnnotation.class);
				//System.out.println(token.word() + " --> corefClusterID = " + corefClustId);

				CorefChain chain = corefs.get(corefClustId);
				
				//ignore tokens with no chain
				if (chain == null) {
					// if (!reprMent.mentionSpan.contains(token.word()))
					resolved.add(token.word());
					continue;
				}

				// pre-processing of chain
				boolean male = false;
				boolean female = false;
				boolean animate = false;
				for (CorefMention m : chain.getMentionsInTextualOrder()) {
					if (m.gender == Dictionaries.Gender.FEMALE) {
						female = true;
					} else if (m.gender == Dictionaries.Gender.MALE) {
						male = true;
					}
					
					if (m.animacy == Dictionaries.Animacy.ANIMATE) {
						animate = true;
					}
				}
				
				//ignore tokens that are not animate or come from a chain with conflicting gender
				if (female && male || !animate) {
					//System.out.println(chain.toString() + " ignored for " + token.word());
					resolved.add(token.word());
					continue;
				} else {
					//replace token with representative mention
					CorefMention reprMent = chain.getRepresentativeMention();
					if (token.index() == reprMent.headIndex && token.sentIndex()+1 == reprMent.sentNum) {
						//is head of representative mention, no need to replace
						resolved.add(token.word());
					} else {
						String j = reprMent.mentionSpan;
						String[] reprWords = j.split(" ");
						
						if (token.tag().equals("PRP$"))	{
							//append "'s" for possessive pronouns
							for (int i = 0; i < reprWords.length-1; i++) {
								resolved.add(reprWords[i]);
							}
							resolved.add(reprWords[reprWords.length-1] + "'s");
						} else {
							for (int i = 0; i < reprWords.length; i++) {
								resolved.add(reprWords[i]);
							}
						}
					}
				}

			}

		}
		
		//remove duplicate words
		for (int i = 1; i < resolved.size(); i++) {
			//System.out.println(resolved.get(i));
			if (resolved.get(i-1).equals(resolved.get(i))) {
				//System.out.println(resolved.get(i) + " removed");
				resolved.remove(i);
				i--;
			} else if ( (resolved.get(i-1).equalsIgnoreCase("the") || resolved.get(i-1).equalsIgnoreCase("a")) 
					&& (resolved.get(i).equalsIgnoreCase("the") || resolved.get(i).equalsIgnoreCase("a")) ) {
				//System.out.println(resolved.get(i) + " removed");
				resolved.remove(i);
				i--;
			}
		}

		String resolvedStr = "";
		if (resolved.size() > 0) {
			String str = resolved.get(0);
			for (String key : decoder.keySet()) {
				if (str.equals(key)) {
					str = decoder.get(key);
				}
			}
			resolvedStr += str + " ";
		}
		for (int i = 1; i < resolved.size(); i++) {
			//fix capitalization following end punctuation
			String str = resolved.get(i);
			String prev = resolved.get(i-1);
			String endPunct = ".!?";
			if (endPunct.contains(prev)) {
				str = str.substring(0, 1).toUpperCase() + str.substring(1);
			}
			
			for (String key : decoder.keySet()) {
				if (str.equals(key)) {
					str = decoder.get(key);
				}
			}
			
			//add word to final string
			resolvedStr += str + " ";
		}

		resolvedStr = cleanOutput(resolvedStr);
		
		resolvedStr.replaceAll("â $", "");

		return resolvedStr;
	}
	
	/**
	 * Removes extraneous spaces in input.
	 * @param resolvedStr - String to clean
	 * @return cleaned string
	 */
	public String cleanOutput(String resolvedStr) {
		// fix spacing around punctuation
		String punct = ".,:;!?'\")]—";
		for (int i = 1; i < resolvedStr.length(); i++) {
			if (punct.contains("" + resolvedStr.charAt(i)) && resolvedStr.charAt(i - 1) == ' ') {
				resolvedStr = resolvedStr.substring(0, i - 1) + resolvedStr.substring(i, resolvedStr.length());
				i--;
			}
		}
		
		String punct2 = "([";
		for (int i = 0; i < resolvedStr.length()-2; i++) {
			if (punct2.contains("" + resolvedStr.charAt(i)) && resolvedStr.charAt(i + 1) == ' ') {
				resolvedStr = resolvedStr.substring(0, i+1) + resolvedStr.substring(i+2, resolvedStr.length());
				i--;
			}
		}

		resolvedStr.trim();
		return resolvedStr;
	}
	
	/**
	 * Checks if any words in the input are a pronoun.
	 * Pronouns = "he", "she", "his", "him", "her", "they", "their"
	 * @param input - input String to check through
	 */
	public void checkForUnresolvedPronouns(String input) {
		Annotation doc = new Annotation(input);
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(doc);

		List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);

		for (CoreMap sentence : sentences) {
			//System.out.println(sentence);
			List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

			for (CoreLabel token : tokens) {
				for (String s : pronouns) {
					if (token.word().equalsIgnoreCase(s)) {
						System.out.println("In sentence: " + sentence);
						System.out.println(token.word() + " at index " + token.index());
					}
				}
			}
		}
	}
	
	//http://stackoverflow.com/questions/4716503/reading-a-plain-text-file-in-java
	/**
	 * Reads a text file into a String.
	 * @param pathname - path of source file to turn into a String
	 * @return file content as a String
	 * @throws IOException
	 */
	private static String readFile(String pathname) throws IOException {
		Reader reader = new InputStreamReader(new FileInputStream(pathname), "UTF-8");
		try(BufferedReader br = new BufferedReader(reader)) {
		    StringBuilder sb = new StringBuilder();
		    String line = br.readLine();

		    while (line != null) {
		        sb.append(line);
		        sb.append(System.lineSeparator());
		        line = br.readLine(); 
		    }
		    String everything = sb.toString();
		    
		    everything = everything.trim();
		    return everything;
		}
	}
	
	/**
	 * Replaces special characters contained in charsToReplace with their corresponding characters.
	 * @param pathname - text file to parse
	 * @throws IOException
	 */
	private static void replaceSpecialCharacters(String pathname) throws IOException {
		String content = readFile(pathname);
		Writer writer = new OutputStreamWriter(new FileOutputStream(pathname), "UTF-8");
		for (int i = 0; i < content.length(); i++) {
			String str = content.substring(i, i+1);
			for (String key : charsToReplace.keySet()) {
				if (str.equals(key)) {
					str = charsToReplace.get(key);
				}
			}
			
			writer.write(str);
		}
		
		writer.close();
	}
	
	/**
	 * Fills charsToReplace with special character string pairs.
	 */
	private static void fillCharsToReplace() {
		charsToReplace.put("—", "--");
		charsToReplace.put("½", "1/2");
		charsToReplace.put("¼", "1/4");
		charsToReplace.put("`", "'");
		charsToReplace.put("’", "'");
		charsToReplace.put("‘", "'");
		charsToReplace.put("“", "\"");
		charsToReplace.put("”", "\"");
	}
	
	/**
	 * Prints all representative mentions for each coref chain in a particular file. (For testing.)
	 * @param filename - input text file
	 * @param pipeline - StanfordCoreNLP object
	 * @throws IOException
	 */
	private static void getRepresentativeMentions(String filename, StanfordCoreNLP pipeline) throws IOException {
		String content = readFile(filename);
		//System.out.println(content);
		Annotation doc = new Annotation(content);
		pipeline.annotate(doc);

		Map<Integer, CorefChain> corefs = doc.get(CorefChainAnnotation.class);
		for (Integer k : corefs.keySet()) {
			CorefChain cc = corefs.get(k);
			
			System.out.println("\n" + cc.toString());
			System.out.println(cc.getRepresentativeMention().mentionSpan + ", headID:" + cc.getRepresentativeMention().headIndex + ", sent:" + cc.getRepresentativeMention().sentNum);
		}
		
	}
}
