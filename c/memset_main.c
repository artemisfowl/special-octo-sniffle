/**
 * @file main.c
 * @author sb
 * @brief program to set up the project workspace baased on the type of the
 * project specified
 */

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>

/* macros section */
#define MAX_ARGS 4
#define MIN_ARGS 2
#define FLAG_LEN 2

#define C_RES	"./res/c"
#define CPP_RES	"./res/cpp"

/* enum */
enum project_t {
	C,			/* default project */
	CPP,
	nentries = 2
};

struct project {
	enum project_t type;
	int rdp_t;		/* read the project type information */
	char *cwd;
	char *prwd;
	char *src;
	char *inc;		/* should not be using these many strings */
	int nfiles;		/* number of files to be copied from rsc */
};

void display_usage(void)
{
	printf("Usage of the program:\n"
			"<program> -t <type> <name_of_project>\n"
			"-t		type of the project\n"
			"-v		display version information\n"
			"-h		display help information\n"
			"-l		display the list of project types\n");
}

void display_version(void)
{
	printf("mkproject v0.0 devel\n");
}

void list_projects(void)
{
	for (int i = 0; i < nentries; i++) {
		switch (i) {
			case C:
				printf("%d. c\n", (i+1));
				break;
			case CPP:
				printf("%d. cpp\n", (i+1));
				break;
			default:
				break;
		}
	}
}

void assign_project_t(char *s, struct project *p)
{
	if (s && p) {
		/* check the string that has been passed and then based on the
		 * string - attach the project type */
		if (!strcmp(s, "c")) {
			p->type = C;
		} else if (!strcmp(s, "cpp")) {
			p->type = CPP;
		}
	}
	return;
}

void parse_flags(char *s, struct project *p)
{
	if (strlen(s) == FLAG_LEN && p) {
		if (*s == '-')
			s++;
		switch (*s) {
			case 'h':
				display_usage();
				exit(EXIT_SUCCESS);
			case 'v':
				display_version();
				exit(EXIT_SUCCESS);
			case 'l':
				list_projects();
				break;
			case 't':
				p->rdp_t = true;
				break;
			default:
				printf("Unrecognised option\n");
				display_usage();
				exit(EXIT_SUCCESS);
		}
	}
	return;
}

void init_project(struct project *p)
{
	if (p) {
		p->type = C;
		p->rdp_t = false;
		p->cwd = NULL;
		p->prwd = NULL;
		p->src = NULL;
		p->inc = NULL;
		p->nfiles = 0;
	}
	return;
}

char **get_file_list(const char *dir_path, char **flist, int *nfiles)
{
	if (dir_path && nfiles) {
		DIR *dir;
		struct dirent *ent;

		if ((dir = opendir(dir_path)) != NULL) {
			printf("List of files in %s\n", dir_path);
			while ((ent = readdir(dir)) != NULL)
				/* make this check with IS_REG */
				if ((strcmp(ent->d_name, ".") > 0) &&
					(strcmp(ent->d_name, "..") > 0))
					(*nfiles)++;
					/*printf("%s\n", ent->d_name);*/
			/* get the number of files present */
			closedir(dir);
			printf("Number of files found : %d\n", *nfiles);

			flist = (char **)malloc((*nfiles) * sizeof(char *));

			/* allocate memory for the number of files */
			/* this part of the code needs to changed */
			for (int i = 0; i < (*nfiles); i++) {
				flist[i] = (char *)malloc(10 * sizeof(char));
				/* implementing a hack of a code */
				memset(flist[i], 'T', strlen(flist[i]));
			}

			/* let's set the memory - may not be required */
			//memset(*flist, 1, *nfiles);

			/* return the file list */
			return flist;
		} else {
			perror("directory could not be opened");
			return NULL;
		}
	} else {
		return NULL;
	}
}

int main(int argc, char *argv[])
{
	/*
	 * todo section here
	 * DONE 1. check the number of arguments provided - recheck
	 * DONE 2. add the code for handling the arguments in else
	 * DONE 3. Check the manpage for getcwd() and then implement getcwd()
	 * DONE 4. Create the project directory
	 * TODO 5. Copy the necessary files inside the project directory
	 * TODO 6. Write a copy function for copying the necessary files
	 * DONE 7. Keep resources in specific resource directories
	 * DONE 8. Fix the issue with init_set mem addrs, use memset
	 */

	struct project p;

	if (argc < MIN_ARGS || argc > MAX_ARGS) {
		printf("Error in number of arguments\n");
		display_usage();
		exit(0);
	} else {
		argc--;
		argv++;
		init_project(&p);

		while(argc--) {
			parse_flags(*argv, &p);
			argv++;
			if (p.rdp_t) {
				assign_project_t(*argv, &p);
				p.rdp_t = false;
				argv++;
				break; /* do not process the project name arg */
			}
		}
	}

	/* now based on the project type the name of the project needs to be
	 * read and then the project structure needs to be set up */
	printf("Name of project : %s\n", *argv); /* this is the project name */

	/* steps to be followed to get the project structure up :
	 * 1. create the directories - src & inc
	 * 2. put the basic Makefile and workspace file in the root directory
	 * 3. make adequate changes to the build ELF filename - this needs to
	 * be done to the Makefile content */

	/* get the name of the current working directory */
	p.cwd = get_current_dir_name();
	printf("Current working directory : %s\n", p.cwd);

	/* get the length of the project name */
	p.prwd = (char *)malloc((strlen(*argv) + strlen(p.cwd) + 2)
			* sizeof(char));

	/* let's see if I can remove the error with uninit values */
	memset(p.prwd, 0, strlen(*argv) + strlen(p.cwd) + 2);

	/* display the final directory path */
	p.prwd = strcat(p.prwd, p.cwd);
	p.prwd = strcat(p.prwd, "/");
	p.prwd = strcat(p.prwd, *argv);
	printf("Project directory location : %s\n", p.prwd);

	/* create the directory now */
	if (!mkdir(p.prwd, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH))
		printf("Directory created successfully\n");
	else
		printf("Directory not created\n");

	/* now create the src/ and the inc/ directories */
	printf("Creating source and include directories\n");
	p.src = (char *)malloc(strlen(p.prwd) + strlen("/src") + 1);
	p.inc = (char *)malloc(strlen(p.prwd) + strlen("/inc") + 1);

	memset(p.src, 0, strlen(p.prwd) + strlen("/src") + 1);
	memset(p.inc, 0, strlen(p.prwd) + strlen("/inc") + 1);

	p.src = strcat(p.src, p.prwd);
	p.src = strcat(p.src, "/src");

	p.inc = strcat(p.inc, p.prwd);
	p.inc = strcat(p.inc, "/inc");

	/* skipping the error check */
	mkdir(p.src, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	mkdir(p.inc, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

	/* time to copy the resources from the respective directory */
	char **flist = NULL;
	flist = get_file_list(C_RES, flist, &p.nfiles);

	/* display the names of the files found */
	if (flist) {
		printf("flist is not NULL\n");
		for (int i = 0; i < p.nfiles; i++)
			printf("Multidm_array_content : %s\n", flist[i]);
	} else {
		printf("flist is NULL\n");
	}

	/* free the resources */
	free(p.cwd);
	free(p.prwd);
	free(p.src);
	free(p.inc);

	/* before freeing the flist - free each and every memory allocated
	 * most probably save the number of files somewhere */
	for (int i = 0; i < p.nfiles; i++)
		free(flist[i]);

	free(flist);

	return 0;
}
