## 🎯 **Complete SDLC Automation Project Prompt Template**

```
Create a comprehensive, production-ready automation solution for [SPECIFIC PROBLEM/TASK] that follows complete Software Development Lifecycle (SDLC) best practices and includes enterprise-grade testing, deployment, and monitoring capabilities.

**CORE REQUIREMENTS:**
- Develops a robust [LANGUAGE] script/application to [PRIMARY FUNCTION]
- Handles [SPECIFIC CRITERIA/CONDITIONS] with intelligent decision-making
- Implements comprehensive error handling, logging, and recovery mechanisms
- Supports multiple execution modes (dry-run, production, debug)
- Provides structured output formats (JSON, XML, CSV) for integration
- Includes comprehensive documentation and user guides

**SDLC IMPLEMENTATION:**

1. **PLANNING & REQUIREMENTS:**
   - Document functional and non-functional requirements
   - Create user stories and acceptance criteria
   - Define success metrics and KPIs
   - Include compliance and security requirements

2. **DESIGN & ARCHITECTURE:**
   - Create modular, maintainable code architecture
   - Implement design patterns (Factory, Strategy, Observer)
   - Design for scalability and extensibility
   - Include configuration management and environment handling

3. **DEVELOPMENT:**
   - Follow coding standards and best practices
   - Implement comprehensive logging and monitoring
   - Include input validation and sanitization
   - Support multiple deployment environments

4. **TESTING (COMPREHENSIVE SUITE):**
   - Unit tests with 90%+ code coverage
   - Integration tests with mocked external dependencies
   - End-to-end workflow testing
   - Performance and load testing scenarios
   - Security and vulnerability testing
   - Compliance validation testing

5. **DEPLOYMENT & CI/CD:**
   - GitHub Actions pipeline with multi-stage deployment
   - Automated testing on every commit/PR
   - Environment-specific deployment (dev/staging/prod)
   - Rollback capabilities and blue-green deployment
   - Infrastructure as Code (IaC) where applicable

6. **MONITORING & MAINTENANCE:**
   - Health checks and monitoring endpoints
   - Performance metrics and alerting
   - Log aggregation and analysis
   - Automated backup and recovery procedures

**INTEGRATION REQUIREMENTS:**
- Push all code to GitHub repository with proper branching strategy
- Register as service in Itential Automation Gateway (IAG) using MCP tools
- Include Docker containerization for consistent deployment
- Implement API endpoints for external integration
- Support webhook notifications and event-driven triggers
- Include database integration where applicable

**BUSINESS IMPACT DOCUMENTATION:**
- Quantify time savings with before/after analysis
- Calculate ROI and cost optimization metrics
- Detail compliance and security improvements
- Demonstrate operational excellence gains
- Provide adoption and change management guidance
- Include executive summary and technical deep-dive sections

**DELIVERABLES:**

📁 **Core Application:**
1. Main automation script/application with enterprise features
2. Configuration management system
3. Dependencies and environment setup
4. CLI and API interfaces

📁 **Testing Suite:**
5. Unit tests with comprehensive coverage
6. Integration tests with realistic scenarios
7. Performance and load testing
8. Security and penetration testing
9. Test automation and reporting tools

📁 **Documentation:**
10. Comprehensive README with quick start guide
11. Technical architecture documentation
12. API documentation (OpenAPI/Swagger)
13. User manual and troubleshooting guide
14. Deployment and operations runbook

📁 **CI/CD & Deployment:**
15. GitHub Actions workflows for CI/CD
16. Docker containers and Kubernetes manifests
17. Infrastructure as Code (Terraform/CloudFormation)
18. Environment-specific configuration
19. Deployment scripts and automation

📁 **Monitoring & Observability:**
20. Health check endpoints
21. Metrics collection and dashboards
22. Logging configuration and analysis
23. Alerting rules and notification setup
24. Performance monitoring and profiling

📁 **Security & Compliance:**
25. Security scanning and vulnerability assessment
26. Compliance validation and reporting
27. Secrets management and encryption
28. Audit trails and access controls
29. Backup and disaster recovery procedures

**ENTERPRISE FEATURES:**
- Multi-tenancy support and isolation
- Role-based access control (RBAC)
- Audit logging and compliance reporting
- High availability and disaster recovery
- Auto-scaling and load balancing
- API rate limiting and throttling
- Data encryption at rest and in transit
- Integration with enterprise identity providers

**ADVANCED CAPABILITIES:**
- Machine learning for predictive analytics
- Real-time event processing and streaming
- GraphQL API for flexible data queries
- Microservices architecture with service mesh
- Event sourcing and CQRS patterns
- Distributed caching and session management
- Message queuing and asynchronous processing

Please provide specific business impact metrics, demonstrate measurable improvements in efficiency, and show how this solution integrates into existing enterprise workflows.
```

---

## 🌟 **What We Accomplished vs. Best Practices**

### ✅ **What We Successfully Implemented:**

1. **Core Application**: ✅ Robust Python script with enterprise features
2. **Unit Testing**: ✅ Comprehensive test suite with 15+ test cases
3. **Integration Testing**: ✅ End-to-end workflow validation with moto
4. **CI/CD Pipeline**: ✅ GitHub Actions with multi-stage deployment
5. **Documentation**: ✅ Extensive README and deployment guides
6. **IAG Integration**: ✅ Service registration and MCP tool usage
7. **Security Scanning**: ✅ Bandit and safety integration
8. **Code Quality**: ✅ Linting, formatting, and type checking
9. **Manual Deployment**: ✅ Production-ready bash scripts
10. **Configuration Management**: ✅ Environment-specific configs

### 🔄 **Additional Good-to-Have Features:**

#### **1. Advanced Testing & Quality Assurance**
```bash
# Performance testing
locust -f tests/performance_tests.py --host=http://iag-host

# Contract testing for API integration
pact-verifier --provider-base-url=http://api-host

# Chaos engineering testing
chaos-monkey --target=aws-iam-rotation --failure-rate=0.1

# Accessibility testing for web interfaces
axe-cli http://dashboard-url

# Browser automation testing
selenium-tests --browser=chrome --headless
```

#### **2. Enhanced Observability & Monitoring**
```yaml
# Prometheus metrics endpoint
/metrics:
  - iam_keys_rotated_total
  - iam_rotation_duration_seconds
  - iam_rotation_errors_total
  - iam_users_processed_total

# Grafana dashboards
dashboards/
├── executive_summary.json
├── operational_metrics.json
├── security_compliance.json
└── performance_analytics.json

# ELK Stack integration
logstash:
  input: filebeat
  filter: grok patterns
  output: elasticsearch

# Application Performance Monitoring
newrelic_agent.ini
datadog_agent.yaml
```

#### **3. Infrastructure as Code**
```hcl
# Terraform for AWS infrastructure
resource "aws_iam_role" "iam_rotation_role" {
  name = "iam-key-rotation-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# CloudFormation for complete stack
Resources:
  IAMRotationLambda:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Code:
        ZipFile: |
          # Lambda function code
```
