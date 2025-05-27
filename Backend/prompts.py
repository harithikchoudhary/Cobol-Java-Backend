"""
Module for generating prompts for code analysis and conversion.
"""

def create_business_requirements_prompt(source_language, source_code, vsam_definition=""):
    """
    Creates a prompt for analyzing business requirements from source code.
    
    Args:
        source_language (str): The programming language of the source code
        source_code (str): The source code to analyze
        vsam_definition (str): Optional VSAM file definition
        
    Returns:
        str: The prompt for business requirements analysis
    """
    vsam_section = ""
    if vsam_definition:
        vsam_section = f"""
        VSAM Definition:
        {vsam_definition}
        """

    return f"""
            You are a business analyst responsible for analyzing and documenting the business requirements from the following {source_language} code and VSAM definition. Your task is to interpret the code's intent and extract meaningful business logic suitable for non-technical stakeholders.

            The code may be written in a legacy language like COBOL, possibly lacking comments or modern structure. You must infer business rules by examining variable names, control flow, data manipulation, and any input/output operations, including VSAM file structures. Focus only on **business intent**—do not describe technical implementation.

            ### Output Format Instructions:
            - Use plain text headings and paragraphs with the following structure:
            - Use '#' for main sections (equivalent to h2)
            - Use '##' for subsection headings (equivalent to h4)
            - Use '###' for regular paragraph text
            - Use '-' for bullet points and emphasize them by using bold tone in phrasing
            - Do not give response with ** anywhere.
            - Do NOT use Markdown formatting like **bold**, _italic_, or backticks

            ### Structure your output into these 5 sections:

            # Overview
            ## Purpose of the System  
            ### Describe the system's primary function and how it fits into the business.
            ## Context and Business Impact  
            ### Explain the operational context and value the system provides.

            # Objectives
            ## Primary Objective  
            ### Clearly state the system's main goal.
            ## Key Outcomes  
            ### Outline expected results (e.g., improved processing speed, customer satisfaction).

            # Business Rules & Requirements
            ## Business Purpose  
            ### Explain the business objective behind this specific module or logic.
            ## Business Rules  
            ### List the inferred rules/conditions the system enforces.
            ## Impact on System  
            ### Describe how this part affects the system's overall operation.
            ## Constraints  
            ### Note any business limitations or operational restrictions.

            # Assumptions & Recommendations
            - Assumptions  
            ### Describe what is presumed about data, processes, or environment.
            - Recommendations  
            ### Suggest enhancements or modernization directions.

            # Expected Output
            ## Output  
            ### Describe the main outputs (e.g., reports, logs, updates).
            ## Business Significance  
            ### Explain why these outputs matter for business processes.
            

            {source_language} Code:
            {source_code}

            {vsam_section}
            """

def create_technical_requirements_prompt(source_language, target_language, source_code, vsam_definition=""):
    """
    Creates a prompt for analyzing technical requirements from source code.
    
    Args:
        source_language (str): The programming language of the source code
        target_language (str): The target programming language for conversion
        source_code (str): The source code to analyze
        vsam_definition (str): Optional VSAM file definition
        
    Returns:
        str: The prompt for technical requirements analysis
    """
    vsam_section = ""
    if vsam_definition:
        vsam_section = f"""
        VSAM Definition:
        {vsam_definition}

        Additional Requirements for VSAM:
        - Analyze VSAM file structures and access methods
        - Map VSAM record layouts to appropriate database tables or data structures
        - Consider VSAM-specific operations (KSDS, RRDS, ESDS) and their equivalents
        - Plan for data migration from VSAM to modern storage
        """

    return f"""
            Analyze the following {source_language} code and extract the technical requirements for migrating it to {target_language}.
            Do not use any Markdown formatting (e.g., no **bold**, italics, or backticks).
            Return plain text only.

            **Focus on implementation details such as:**
            "1. Examine the entire codebase first to understand architectural patterns and dependencies.\n"
            "2. Analyze code in logical sections, mapping technical components to system functions.\n"
            "3. For each M204 or COBOL-specific construct, identify the exact technical requirement it represents.\n"
            "4. Document all technical constraints, dependencies, and integration points.\n"
            "5. Pay special attention to error handling, transaction management, and data access patterns.\n\n"
            "kindat each requirement as 'The system must [specific technical capability]' or 'The system should [specific technical capability]' with direct traceability to code sections.\n\n"
            "Ensure your output captures ALL technical requirements including:\n"
            "- Data structure definitions and relationships\n"
            "- Processing algorithms and computation logic\n"
            "- I/O operations and file handling\n"
            "- Error handling and recovery mechanisms\n"
            "- Performance considerations and optimizations\n"
            "- Security controls and access management\n"
            "- Integration protocols and external system interfaces\n"
            "- Database Interactions and equivalent in target language\n"
            "- VSAM file structures and their modern equivalents\n"


            Format your response as a numbered list with '# Technical Requirements' as the title.
            Each requirement should start with a number followed by a period (e.g., "1.", "2.", etc.)

            {source_language} Code:
            {source_code}

            {vsam_section}
             """

def create_java_code_conversion_prompt(
    source_language,
    source_code,
    business_requirements,
    technical_requirements,
    db_setup_template,
    vsam_definition="",
    is_chunk=False,
    chunk_type="mixed",
    chunk_index=0,
    total_chunks=1
):
    """
    Creates a prompt for converting code from any language to Java.
    Enforces Spring Boot layered architecture output format.

    Args:
        source_language (str): The programming language of the source code
        source_code (str): The source code to convert
        business_requirements (str): The business requirements extracted from analysis
        technical_requirements (str): The technical requirements extracted from analysis
        db_setup_template (str): The database setup template for Java/Spring Boot
        vsam_definition (str): Optional VSAM file definition
        is_chunk (bool): Whether the code is a chunk of a larger program
        chunk_type (str): Type of chunk ('declarations', 'procedures', or 'mixed')
        chunk_index (int): Index of current chunk (0-based)
        total_chunks (int): Total number of chunks

    Returns:
        str: The prompt for Java code conversion
    """
    vsam_section = ""
    if vsam_definition:
        vsam_section = f"""
        **VSAM Definition:**
        {vsam_definition}

        **VSAM-Specific Instructions:**
        - Convert VSAM file structures to appropriate JPA entities and database tables
        - Map VSAM operations to Spring Data JPA repository methods
        - Maintain VSAM-like functionality (KSDS, RRDS, ESDS) using modern JPA/Hibernate
        - Ensure data integrity and transaction management using @Transactional
        """

    base_prompt = f"""
        **Important- Please ensure that the {source_language} code is translated into its exact equivalent in Java, maintaining a clean Spring Boot layered architecture.**
    Convert the following {source_language} code to Java using Spring Boot framework while strictly adhering to the provided business and technical requirements.

    **Source Language:** {source_language}
    **Target Language:** Java (Spring Boot)

    **Required Java Spring Boot Output Structure:**
    
    Your response must be organized in the following sections, each clearly marked with a section header:

    ##Entity
    FileName: [EntityName].java
    - Define JPA entities with @Entity annotation
    - Include @Id, @GeneratedValue, @Column annotations
    - Define all properties with appropriate data types
    - Include relationships (@OneToMany, @ManyToOne, etc.)
    - Add validation annotations (@NotNull, @Size, etc.)
    - Include constructors, getters, and setters

    ##Repository
    FileName: [EntityName]Repository.java
    - Extend JpaRepository<Entity, ID> or CrudRepository
    - Define custom query methods using @Query annotation
    - Include method signatures for CRUD operations
    - Add @Repository annotation

    ##Service
    FileName: [EntityName]Service.java
    - Implement service interface with @Service annotation
    - Include business logic and validation
    - Use @Autowired for dependency injection
    - Add @Transactional for database operations
    - Include error handling and exception management

    ##Controller
    FileName: [EntityName]Controller.java
    - Define REST endpoints with @RestController annotation
    - Include @RequestMapping for base path
    - Define methods with @GetMapping, @PostMapping, @PutMapping, @DeleteMapping
    - Include @RequestBody, @PathVariable, @RequestParam annotations
    - Add proper HTTP response handling with ResponseEntity
    - Include validation with @Valid annotation

    ##application.properties
    - Database connection configuration (spring.datasource.*)
    - JPA/Hibernate settings (spring.jpa.*)
    - Connection pool settings (spring.datasource.hikari.*)
    - Server port and context path settings

    ##Dependencies
    - Spring Boot parent dependency
    - Spring Boot starter dependencies (web, data-jpa, etc.)
    - Database driver dependencies
    - Connection pool dependencies
    - Testing dependencies

    Each section must be clearly separated using the above headers. Include only relevant code for each layer.
    Ensure proper dependency injection and relationships between layers are maintained.
   
    {vsam_section}
    """
    
    if is_chunk:
        base_prompt += f"""
    **IMPORTANT CHUNKING INFORMATION:**
    This code is chunk {chunk_index + 1} of {total_chunks} from a larger {source_language} program.
    Chunk type identified as: {chunk_type}
    """
        
        if chunk_type == "declarations":
            base_prompt += f"""
    **Instructions for Declarations Chunk:**
    - Focus ONLY on converting data structures to JPA entities in this chunk
    - Generate appropriate @Entity classes with proper annotations
    - Create repository interfaces extending JpaRepository
    - If needed, create service interface skeletons but DO NOT implement full methods
    - Ensure your output can be combined with other chunks (proper package structure)
    - Only include application.properties and pom.xml if this is the first chunk (chunk {chunk_index + 1})
    - If this is chunk 1, generate Application.java main class
    - DO NOT add any "placeholder" or "to be implemented" comments for other chunks
    """
        
        elif chunk_type == "procedures":
            base_prompt += f"""
    **Instructions for Procedures Chunk:**
    - Focus ONLY on converting the business logic to service implementations and controllers
    - Ensure method implementations maintain the exact behavior as the original
    - Create service implementations with @Service annotation
    - Create REST controllers with appropriate mappings
    - Assume entity classes and repositories are handled in other chunks
    - DO NOT include application.properties or pom.xml unless specific to this procedure
    - DO NOT duplicate main application class from previous chunks
    """
        
        else:  # mixed type
            base_prompt += f"""
    **Instructions for Mixed Content Chunk:**
    - Convert BOTH entities and business logic as appropriate
    - Create complete layers (Entity, Repository, Service, Controller) for this chunk
    - Only include Application.java and configuration if it's actually in this chunk's source code
    - If this is chunk 1, include appropriate Spring Boot application structure
    - If this chunk contains multiple business processes, organize them properly
    """
            
        base_prompt += f"""
    **Chunking Guidelines for Java:**
    - Generate ONLY code for this specific chunk - don't try to complete the entire application
    - Ensure proper package structure (com.example.app.entity, com.example.app.service, etc.)
    - Maintain consistent naming across chunks following Java conventions
    - If this chunk references classes defined in other chunks, use proper imports
    """
    
    base_prompt += f"""
    **Java-Specific Requirements:**
    - Produce a complete, executable Spring Boot implementation
    - Follow Java naming conventions (PascalCase for classes, camelCase for methods/variables)
    - Use appropriate Spring Boot annotations and configurations
    - Include proper exception handling with custom exceptions if needed
    - Implement proper validation using Bean Validation annotations
    - Use ResponseEntity for REST endpoints with appropriate HTTP status codes
    - Maintain all business logic, functionality, and behavior of the original code
    - DO NOT include markdown code blocks (like ```java) in your response, just provide the raw code
    - Do not return any unwanted code or functions which are not in {source_language}.

    **Spring Boot Best Practices:**
    - Use constructor injection over field injection
    - Implement proper error handling and logging
    - Use DTOs for API requests/responses when appropriate
    - Follow RESTful API design principles
    - Include proper transaction management with @Transactional

    **Database-Specific Instructions for Java:**
    - Use Spring Data JPA for database operations
    - Create appropriate JPA entities with proper relationships
    - Use Hibernate as the JPA implementation
    """
    
    # Only include DB setup template for first chunk or if it's a single chunk
    if not is_chunk or chunk_index == 0:
        base_prompt += f"""
    - Follow this example format for Spring Boot database configuration:

    {db_setup_template if db_setup_template else 'Standard Spring Boot JPA configuration will be used.'}
    """
    else:
        base_prompt += f"""
    - DO NOT include database configuration as it should be in chunk 1
    """

    # Include business and technical requirements for context
    base_prompt += f"""
    **Business Requirements:**
    {business_requirements if business_requirements else 'None provided.'}

    **Technical Requirements:**
    {technical_requirements if technical_requirements else 'None provided.'}

    **Source Code ({source_language}{' - CHUNK ' + str(chunk_index + 1) + ' of ' + str(total_chunks) if is_chunk else ''}):**
    {source_code}

    IMPORTANT: Only return the complete converted Java code WITHOUT any markdown formatting. DO NOT wrap your code in triple backticks (```). Return just the raw code itself.
    """

    if is_chunk:
        # Add additional reminder for chunked processing
        base_prompt += f"""
    REMINDER: You are converting ONLY CHUNK {chunk_index + 1} of {total_chunks}. Do not try to implement logic from other chunks.
    For database-related operations, only include Spring Boot configuration if this is chunk 1 or if the database operations 
    are specifically in this chunk.
    """

    base_prompt += f"""
    **Additional Spring Boot Setup Instructions:**
    If database operations are detected in the source code, include these files in your output:

    ##application.properties
    Example configuration:
    spring.datasource.url=jdbc:h2:mem:testdb
    spring.datasource.driverClassName=org.h2.Driver
    spring.datasource.username=sa
    spring.datasource.password=password
    spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
    spring.jpa.hibernate.ddl-auto=update
    spring.jpa.show-sql=true
    server.port=8080

    ##pom.xml
    Required dependencies:
    - spring-boot-starter-web
    - spring-boot-starter-data-jpa
    - spring-boot-starter-validation
    - Database driver (H2, MySQL, PostgreSQL, etc.)
    - spring-boot-starter-test
    """

    return base_prompt

def create_csharp_code_conversion_prompt(
    source_language,
    source_code,
    business_requirements,
    technical_requirements,
    db_setup_template,
    vsam_definition="",
    is_chunk=False,
    chunk_type="mixed",
    chunk_index=0,
    total_chunks=1
):
    """
    Creates a prompt for converting code from any language to C#.
    Enforces .NET Core/ASP.NET Core layered architecture output format.

    Args:
        source_language (str): The programming language of the source code
        source_code (str): The source code to convert
        business_requirements (str): The business requirements extracted from analysis
        technical_requirements (str): The technical requirements extracted from analysis
        db_setup_template (str): The database setup template for C#/.NET Core
        vsam_definition (str): Optional VSAM file definition
        is_chunk (bool): Whether the code is a chunk of a larger program
        chunk_type (str): Type of chunk ('declarations', 'procedures', or 'mixed')
        chunk_index (int): Index of current chunk (0-based)
        total_chunks (int): Total number of chunks

    Returns:
        str: The prompt for C# code conversion
    """
    vsam_section = ""
    if vsam_definition:
        vsam_section = f"""
        **VSAM Definition:**
        {vsam_definition}

        **VSAM-Specific Instructions:**
        - Convert VSAM file structures to appropriate Entity Framework models and database tables
        - Map VSAM operations to Entity Framework repository methods
        - Maintain VSAM-like functionality (KSDS, RRDS, ESDS) using modern EF Core patterns
        - Ensure data integrity and transaction management using Entity Framework transactions
        """

    base_prompt = f"""
        **Important- Please ensure that the {source_language} code is translated into its exact equivalent in C#, maintaining a clean .NET Core layered architecture.**
    Convert the following {source_language} code to C# using .NET Core/ASP.NET Core framework while strictly adhering to the provided business and technical requirements.

    **Source Language:** {source_language}
    **Target Language:** C# (.NET Core/ASP.NET Core)

    **Required C# .NET Core Output Structure:**
    
    Your response must be organized in the following sections, each clearly marked with a section header:

    ##Models/Entities
    FileName: [EntityName].cs
    - Define Entity Framework models with appropriate attributes
    - Include [Key], [Column], [Table], [Required] attributes
    - Define all properties with appropriate C# data types
    - Include navigation properties for relationships
    - Add data validation attributes ([StringLength], [Range], etc.)
    - Include constructors and property accessors

    ##Data/DbContext
    FileName: ApplicationDbContext.cs
    - Inherit from DbContext
    - Define DbSet<Entity> properties for each entity
    - Override OnModelCreating for entity configuration
    - Include connection string configuration

    ##Repositories/Interfaces
    FileName: I[EntityName]Repository.cs
    - Define repository interface with CRUD method signatures
    - Include custom query method signatures
    - Follow repository pattern principles

    ##Repositories/Implementations  
    FileName: [EntityName]Repository.cs
    - Implement repository interface
    - Inject ApplicationDbContext via constructor
    - Implement CRUD operations using Entity Framework
    - Include async/await patterns for database operations
    - Add error handling and logging

    ##Services/Interfaces
    FileName: I[EntityName]Service.cs
    - Define service interface with business method signatures
    - Include business logic method definitions

    ##Services/Implementations
    FileName: [EntityName]Service.cs
    - Implement service interface
    - Inject repository dependencies via constructor
    - Include business logic and validation
    - Use async/await for database operations
    - Add proper exception handling and logging
    - Include transaction management where needed

    ##Controllers
    FileName: [EntityName]Controller.cs
    - Inherit from ControllerBase or Controller
    - Add [ApiController] and [Route] attributes
    - Define action methods with [HttpGet], [HttpPost], [HttpPut], [HttpDelete]
    - Include [FromBody], [FromRoute], [FromQuery] parameter attributes
    - Use ActionResult<T> return types
    - Inject service dependencies via constructor
    - Add model validation with ModelState
    - Include proper HTTP status code responses

    ##Program.cs
    - Configure services and dependency injection
    - Add Entity Framework DbContext configuration
    - Configure middleware pipeline
    - Include CORS, authentication, and other middleware as needed

    ##appsettings.json
    - Database connection strings
    - Application configuration settings
    - Logging configuration
    - Environment-specific settings

    ##[ProjectName].csproj
    - Target framework (net6.0 or net8.0)
    - Package references for Entity Framework Core
    - Database provider packages
    - ASP.NET Core packages
    - Additional required NuGet packages

    ##Startup.cs
    - ConfigureServices method for service registration
    - Configure method for middleware configuration
    

    Each section must be clearly separated using the above headers. Include only relevant code for each layer.
    Ensure proper dependency injection and relationships between layers are maintained.
   
    {vsam_section}
    """
    
    if is_chunk:
        base_prompt += f"""
    **IMPORTANT CHUNKING INFORMATION:**
    This code is chunk {chunk_index + 1} of {total_chunks} from a larger {source_language} program.
    Chunk type identified as: {chunk_type}
    """
        
        if chunk_type == "declarations":
            base_prompt += f"""
    **Instructions for Declarations Chunk:**
    - Focus ONLY on converting data structures to Entity Framework models in this chunk
    - Generate appropriate model classes with EF attributes
    - Create DbContext with DbSet properties
    - Create repository interfaces but DO NOT implement full repository classes
    - Ensure your output can be combined with other chunks (proper namespace structure)
    - Only include appsettings.json and .csproj if this is the first chunk (chunk {chunk_index + 1})
    - If this is chunk 1, generate Program.cs with basic configuration
    - DO NOT add any "placeholder" or "to be implemented" comments for other chunks
    """
        
        elif chunk_type == "procedures":
            base_prompt += f"""
    **Instructions for Procedures Chunk:**
    - Focus ONLY on converting the business logic to service implementations and controllers
    - Ensure method implementations maintain the exact behavior as the original
    - Create service implementations and repository implementations
    - Create API controllers with appropriate action methods
    - Assume model classes and DbContext are handled in other chunks
    - DO NOT include appsettings.json or .csproj unless specific to this procedure
    - DO NOT duplicate Program.cs configuration from previous chunks
    """
        
        else:  # mixed type
            base_prompt += f"""
    **Instructions for Mixed Content Chunk:**
    - Convert BOTH models and business logic as appropriate
    - Create complete layers (Models, Repositories, Services, Controllers) for this chunk
    - Only include Program.cs and configuration if it's actually in this chunk's source code
    - If this is chunk 1, include appropriate .NET Core application structure
    - If this chunk contains multiple business processes, organize them properly
    """
            
        base_prompt += f"""
    **Chunking Guidelines for C#:**
    - Generate ONLY code for this specific chunk - don't try to complete the entire application
    - Ensure proper namespace structure (ProjectName.Models, ProjectName.Services, etc.)
    - Maintain consistent naming across chunks following C# conventions
    - If this chunk references classes defined in other chunks, use proper using statements
    """
    
    base_prompt += f"""
    **C#-Specific Requirements:**
    - Produce a complete, executable .NET Core application
    - Follow C# naming conventions (PascalCase for classes/methods/properties, camelCase for fields/parameters)
    - Use appropriate .NET Core attributes and configurations
    - Include proper exception handling with custom exceptions if needed
    - Implement async/await patterns for I/O operations
    - Use ActionResult<T> for controller action return types
    - Use dependency injection throughout the application
    - Maintain all business logic, functionality, and behavior of the original code
    - DO NOT include markdown code blocks (like ```csharp) in your response, just provide the raw code
    - Do not return any unwanted code or functions which are not in {source_language}.

    **.NET Core Best Practices:**
    - Use constructor injection for dependency injection
    - Implement proper error handling and logging using ILogger
    - Use DTOs/ViewModels for API requests/responses when appropriate
    - Follow RESTful API design principles
    - Include proper model validation using Data Annotations
    - Use async/await consistently for database operations
    - Implement proper disposal patterns for resources

    **Database-Specific Instructions for C#:**
    - Use Entity Framework Core for database operations
    - Create appropriate Entity Framework models with proper relationships
    - Use Code First approach with migrations
    """
    
    # Only include DB setup template for first chunk or if it's a single chunk
    if not is_chunk or chunk_index == 0:
        base_prompt += f"""
    - Follow this example format for .NET Core database configuration:

    {db_setup_template if db_setup_template else 'Standard Entity Framework Core configuration will be used.'}
    """
    else:
        base_prompt += f"""
    - DO NOT include database configuration as it should be in chunk 1
    """

    # Include business and technical requirements for context
    base_prompt += f"""
    **Business Requirements:**
    {business_requirements if business_requirements else 'None provided.'}

    **Technical Requirements:**
    {technical_requirements if technical_requirements else 'None provided.'}

    **Source Code ({source_language}{' - CHUNK ' + str(chunk_index + 1) + ' of ' + str(total_chunks) if is_chunk else ''}):**
    {source_code}

    IMPORTANT: Only return the complete converted C# code WITHOUT any markdown formatting. DO NOT wrap your code in triple backticks (```). Return just the raw code itself.
    """

    if is_chunk:
        # Add additional reminder for chunked processing
        base_prompt += f"""
    REMINDER: You are converting ONLY CHUNK {chunk_index + 1} of {total_chunks}. Do not try to implement logic from other chunks.
    For database-related operations, only include .NET Core configuration if this is chunk 1 or if the database operations 
    are specifically in this chunk.
    """

    base_prompt += f"""
    **Additional .NET Core Setup Instructions:**
    If database operations are detected in the source code, include these files in your output:

    ##appsettings.json
    Example configuration:
    {{
      "ConnectionStrings": {{
        "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=YourAppDb;Trusted_Connection=true;MultipleActiveResultSets=true"
      }},
      "Logging": {{
        "LogLevel": {{
          "Default": "Information",
          "Microsoft.AspNetCore": "Warning"
        }}
      }},
      "AllowedHosts": "*"
    }}

    ##[ProjectName].csproj
    Required package references:
    - Microsoft.AspNetCore.App (framework reference)
    - Microsoft.EntityFrameworkCore
    - Microsoft.EntityFrameworkCore.SqlServer (or other provider)
    - Microsoft.EntityFrameworkCore.Tools
    - Microsoft.EntityFrameworkCore.Design
    """

    return base_prompt

def create_code_conversion_prompt(
    source_language,
    target_language,
    source_code,
    business_requirements,
    technical_requirements,
    db_setup_template,
    vsam_definition="",
    is_chunk=False,
    chunk_type="mixed",
    chunk_index=0,
    total_chunks=1
):
    """
    Creates a prompt for converting code from one language to another.
    Now enforces a layered architecture output format.

    Args:
        source_language (str): The programming language of the source code
        target_language (str): The target programming language for conversion
        source_code (str): The source code to convert
        business_requirements (str): The business requirements extracted from analysis
        technical_requirements (str): The technical requirements extracted from analysis
        db_setup_template (str): The database setup template for the target language
        vsam_definition (str): Optional VSAM file definition
        is_chunk (bool): Whether the code is a chunk of a larger COBOL program
        chunk_type (str): Type of chunk ('declarations', 'procedures', or 'mixed')
        chunk_index (int): Index of current chunk (0-based)
        total_chunks (int): Total number of chunks

    Returns:
        str: The prompt for code conversion
    """
    vsam_section = ""
    if vsam_definition:
        vsam_section = f"""
        **VSAM Definition:**
        {vsam_definition}

        **VSAM-Specific Instructions:**
        - Convert VSAM file structures to appropriate database tables or data structures
        - Map VSAM operations to equivalent database operations
        - Maintain VSAM-like functionality (KSDS, RRDS, ESDS) using modern storage
        - Ensure data integrity and transaction management
        """

    base_prompt = f"""
        **Important- Please ensure that the {source_language} code is translated into its exact equivalent in {target_language}, maintaining a clean layered architecture.**
    Convert the following {source_language} code to {target_language} while strictly adhering to the provided business and technical requirements.

    **Source Language:** {source_language}
    **Target Language:** {target_language}

    **Required Output Structure:**
    
    Your response must be organized in the following sections, each clearly marked with a section header:

    
    ##Entity
    FileName: 
    - Define all entities and their properties
    - Define all domain entities/models
    - Include all necessary properties and relationships
    - Add appropriate annotations/decorators

    ##Repository
    FileName: 
    - Define repository interfaces
    - Include necessary data access methods
    - Add appropriate annotations/decorators


    ##Service
    FileName: 
    - Define service interfaces and implementations
    - Include business logic and transaction management
    - Add appropriate dependency injections and annotations

    ##Controller
    FileName: 
    - Define REST endpoints or API controllers
    - Include request/response handling
    - Add appropriate route mappings and annotations

    ##application.properties
    - Include database connection configuration
    - Include JPA/Hibernate settings
    - Include connection pool settings

    ##Dependencies
    - Include all necessary dependencies
    - Include database dependencies
    - Include ORM dependencies


    Each section must be clearly separated using the above headers. Include only relevant code for each layer.
    Ensure proper dependency injection and relationships between layers are maintained.
   

    {vsam_section}
    """
    
    if is_chunk:
        base_prompt += f"""
    **IMPORTANT CHUNKING INFORMATION:**
    This code is chunk {chunk_index + 1} of {total_chunks} from a larger {source_language} program.
    Chunk type identified as: {chunk_type}
    """
        
        if chunk_type == "declarations":
            base_prompt += f"""
    **Instructions for Declarations Chunk:**
    - Focus ONLY on converting data structures, file definitions, and variable declarations in this chunk
    - Generate appropriate class structures, fields, and data types in {target_language}
    - If needed, create class skeletons but DO NOT implement full methods
    - Ensure your output can be combined with other chunks (proper scoping)
    - Only include database connection setup code if this is the first chunk (chunk {chunk_index + 1})
    - If this is chunk 1, generate appropriate overall program structure
    - DO NOT add any "placeholder" or "to be implemented" comments for other chunks
    """
        
        elif chunk_type == "procedures":
            base_prompt += f"""
    **Instructions for Procedures Chunk:**
    - Focus ONLY on converting the business logic and procedures in this chunk
    - Ensure method implementations and logic maintain the exact behavior as the original
    - Only include necessary method/function definitions needed for this specific chunk
    - Assume data declarations are handled in other chunks
    - DO NOT include database connection code unless it's specifically part of this procedure chunk
    - DO NOT duplicate database initialization that might have been in previous chunks
    """
        
        else:  # mixed type
            base_prompt += f"""
    **Instructions for Mixed Content Chunk:**
    - Convert BOTH declarations and procedures in this chunk as appropriate
    - Maintain the structure and relationship between declarations and procedures
    - Only include database initialization if it's actually in this chunk's source code
    - If this is chunk 1, include appropriate program structure and entry points
    - If this chunk contains multiple procedures, ensure they're properly organized
    """
            
        base_prompt += f"""
    **Chunking Guidelines:**
    - Generate ONLY code for this specific chunk - don't try to complete the entire program
    - Ensure your code fragment is syntactically correct on its own
    - Maintain consistent naming across chunks (follow naming patterns in the source)
    - If this chunk references variables/methods defined in other chunks, continue using those names
    """
    
    base_prompt += f"""
    **Requirements:**
    - The output should be a complete, executable implementation in the target language
    - Maintain all business logic, functionality, and behavior of the original code
    - Produce idiomatic code following best practices in the target language
    - Include all necessary class definitions, method implementations, and boilerplate code
    - Ensure consistent data handling, formatting, and computations
    - DO NOT include markdown code blocks (like ```java or ```) in your response, just provide the raw code
    - Do not return any unwanted code in {target_language} or functions which are not in {source_language}.

    **Language-Specific Instructions:**
    - If converting to Java: Produce a fully functional and idiomatic Java implementation with appropriate class structures
    - If converting to C#: Produce a fully functional and idiomatic C# implementation that matches the original behavior exactly

    **Database-Specific Instructions**
    - If the {source_language} code includes any database-related operations, automatically generate the necessary setup code
    """
    
    # Only include DB setup template for first chunk or if it's a single chunk
    if not is_chunk or chunk_index == 0:
        base_prompt += f"""
    - Follow this example format for database initialization and setup:

    {db_setup_template if db_setup_template else 'No database setup required.'}
    """
    else:
        base_prompt += f"""
    - DO NOT include database initialization code as it should be in chunk 1
    """

    # Include business and technical requirements for context
    base_prompt += f"""
    **Business Requirements:**
    {business_requirements if business_requirements else 'None provided.'}

    **Technical Requirements:**
    {technical_requirements if technical_requirements else 'None provided.'}

    **Source Code ({source_language}{' - CHUNK ' + str(chunk_index + 1) + ' of ' + str(total_chunks) if is_chunk else ''}):**
    {source_code}

    IMPORTANT: Only return the complete converted code WITHOUT any markdown formatting. DO NOT wrap your code in triple backticks (```). Return just the raw code itself.
    """

    if is_chunk:
        # Add additional reminder for chunked processing
        base_prompt += f"""
    REMINDER: You are converting ONLY CHUNK {chunk_index + 1} of {total_chunks}. Do not try to implement logic from other chunks.
    For database-related operations, only include connection initialization if this is chunk 1 or if the database operations 
    are specifically in this chunk.
    """

    base_prompt += f"""
    **Additional Database Setup Instructions:**
    If database operations are detected in the source code, include these files in your output:

    ##application.properties
    - Database connection configuration
    - JPA/Hibernate settings
    - Connection pool settings

    ##Dependencies
    - Required database dependencies
    - Connection pool dependencies
    - ORM dependencies
    """

    return base_prompt


def create_unit_test_prompt(target_language, converted_code, business_requirements, technical_requirements):
    """Create a prompt for generating unit tests for the converted code"""
    
    prompt = f"""
    You are tasked with creating comprehensive unit tests for newly converted {target_language} code.
    
    Please generate unit tests for the following {target_language} code. The tests should verify that 
    the code meets all business requirements and handles edge cases appropriately.
    
    Business Requirements:
    {business_requirements}
    
    Technical Requirements:
    {technical_requirements}
    
    Converted Code ({target_language}):
    
    ```
    {converted_code}
    ```
    
    Guidelines for the unit tests:
    1. Use appropriate unit testing framework for {target_language} (e.g., JUnit for Java, NUnit/xUnit for C#)
    2. Create tests for all public methods and key functionality
    3. Include positive test cases, negative test cases, and edge cases
    4. Use mocks/stubs for external dependencies where appropriate
    5. Follow test naming conventions that clearly describe what is being tested
    6. Include setup and teardown as needed
    7. Add comments explaining complex test scenarios
    8. Ensure high code coverage, especially for complex business logic
    
    Provide ONLY the unit test code without additional explanations.
    """
    
    return prompt


def create_functional_test_prompt(target_language, converted_code, business_requirements):
    """Create a prompt for generating functional test cases based on business requirements"""
    
    prompt = f"""
    You are tasked with creating functional test cases for a newly converted {target_language} application.
    Give response of functional tests in numeric plain text numbering.
    
    Please generate comprehensive functional test cases that verify the application meets all business requirements.
    These test cases will be used by QA engineers to validate the application functionality.
    
    Business Requirements:
    {business_requirements}
    
    Converted Code ({target_language}):
    
    ```
    {converted_code}
    ```
    
    Guidelines for functional test cases:
    1. Create test cases that cover all business requirements
    2. Organize test cases by feature or business functionality
    3. For each test case, include:
       a. Test ID and title
       b. Description/objective
       c. Preconditions
       d. Test steps with clear instructions
       e. Expected results
       f. Priority (High/Medium/Low)
    4. Include both positive and negative test scenarios
    5. Include test cases for boundary conditions and edge cases
    6. Create end-to-end test scenarios that cover complete business processes
    
    Format your response as a structured test plan document with clear sections and test case tables.
    Return the respons ein JSON FORMA
    """
    
    return prompt