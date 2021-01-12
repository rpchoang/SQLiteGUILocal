setup(
		name = "lordstown-materials-database=editor",
		version="1.0.0",
		description = "Explore the materials database and look at its properties",
		long_description = README,
		long_description_content_type="text/markdown",
		url = "https://github.com/ronhoang/LordstownMaterialsDatabase",
		author="Ronald Hoang",
		author_email="rpchoang@gmail.com",
		classifiers=[
			"Programming Language :: Python",
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 3",
			],
		packages = ["LMCGui"],
		include_package_data = True,
		entry_points={"console_scripts": ["LMCSQLGui=SQLiteGUI.__main__:main"]},

)