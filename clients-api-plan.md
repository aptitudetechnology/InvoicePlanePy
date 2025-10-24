# Clients API Implementation Plan (Read-Only)

## Overview
This document outlines the plan to implement a **read-only JSON API for client management** in InvoicePlanePy, enabling the Business Plugin Middleware to programmatically access client/contact information without the ability to modify data.

## Current State Analysis

### ✅ What Exists
- **Client Model**: Complete SQLAlchemy model with contact fields (phone, email, address, etc.)
- **Web Interface**: Full CRUD operations via HTML templates
- **Database Schema**: Clients table with all necessary fields
- **Authentication**: API key and JWT authentication systems

### ❌ What's Missing
- **JSON API Endpoints**: No `/clients/api` endpoints for programmatic access
- **API Documentation**: Clients API marked as "planned for future release"

## Requirements (Read-Only Focus)

### Functional Requirements
1. **List Clients**: Paginated client listing with search and filtering
2. **Get Client Details**: Retrieve complete client information including contact details
3. **Search & Filter**: Search by name, email, phone, company
4. **Contact Access**: Read multiple contact methods per client

### Technical Requirements
1. **RESTful Design**: GET methods only for read operations
2. **JSON Responses**: Consistent JSON format matching existing APIs
3. **Authentication**: Support API key authentication
4. **Validation**: Input validation and error handling
5. **Pagination**: Consistent pagination like invoices API
6. **Filtering**: Status, search, sorting capabilities

## Database Schema Assessment

### Current Client Table Structure
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    is_active BOOLEAN DEFAULT TRUE,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100),
    language VARCHAR(10) DEFAULT 'en',
    address_1 VARCHAR(255),
    address_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(50),
    phone VARCHAR(20),
    fax VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    gender VARCHAR(10),
    birthdate DATE,
    company VARCHAR(255),
    vat_id VARCHAR(50),
    tax_code VARCHAR(50),
    abn VARCHAR(50),
    title VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Schema Status: ✅ No Changes Required
The existing client table already contains all necessary fields for contact information. No database migrations needed.

## API Endpoints Design (Read-Only)

### 1. GET /clients/api - List Clients
**Purpose**: Retrieve paginated list of clients with optional filtering and search.

**Query Parameters**:
- `page` (int, default: 1): Page number
- `limit` (int, default: 100, max: 1000): Items per page
- `search` (string, optional): Search in name, email, company, phone
- `is_active` (boolean, optional): Filter by active status (default: true)
- `sort_by` (string, default: "name"): Sort field (name, email, company, created_at)
- `sort_order` (string, default: "asc"): Sort order (asc, desc)

**Response Format**:
```json
{
  "clients": [
    {
      "id": 1,
      "is_active": true,
      "name": "John Doe",
      "surname": "Smith",
      "company": "Acme Corp",
      "email": "john@acme.com",
      "phone": "+1-555-0123",
      "mobile": "+1-555-0456",
      "fax": "+1-555-0789",
      "website": "https://acme.com",
      "address_1": "123 Main St",
      "address_2": "Suite 100",
      "city": "Anytown",
      "state": "CA",
      "zip_code": "12345",
      "country": "USA",
      "language": "en",
      "gender": "male",
      "birthdate": "1980-01-15",
      "vat_id": "US123456789",
      "tax_code": "TX123",
      "notes": "Preferred customer",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:15:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 100,
    "total": 150,
    "total_pages": 2
  },
  "filters": {
    "search": null,
    "is_active": true,
    "sort_by": "name",
    "sort_order": "asc"
  }
}
```

### 2. GET /clients/{client_id}/api - Get Client Details
**Purpose**: Retrieve complete information for a specific client.

**Response Format**: Single client object (same structure as above).

## Implementation Steps (Simplified Read-Only)

### Single Phase: Core Read-Only API (Priority: High)
1. **Create API Router Structure**
   - Add JSON API endpoints to `app/routers/clients.py`
   - Follow existing patterns from `invoices.py`

2. **Implement GET /clients/api**
   - Add pagination, filtering, and search logic
   - Return JSON response with client data
   - Include proper error handling

3. **Implement GET /clients/{client_id}/api**
   - Add path parameter validation
   - Return single client or 404 error

4. **Add Authentication & Permissions**
   - Ensure API key authentication works
   - Add admin-only restrictions if needed

## Testing Strategy

### Unit Tests
- Test each endpoint with valid/invalid inputs
- Test authentication and authorization
- Test pagination and filtering logic
- Test error handling scenarios

### Integration Tests
- Test with Business Plugin Middleware
- Test with various client data scenarios

### API Testing Examples
```bash
# List clients
curl -X GET "http://localhost:8000/clients/api?page=1&limit=10&search=john" \
  -H "Authorization: Bearer sk_your_api_key"

# Get specific client
curl -X GET "http://localhost:8000/clients/123/api" \
  -H "Authorization: Bearer sk_your_api_key"
```

## Documentation Updates

### API Specification Updates
1. **Update INVOICEPLANEPY_API_SPECIFICATION.md**
   - Replace "planned for future release" note
   - Add complete endpoint documentation for read-only operations
   - Include request/response examples
   - Add error code documentation

2. **Add Usage Examples**
   - Business Plugin Middleware integration examples
   - Client data synchronization scenarios

## Migration Strategy

### Backward Compatibility
- Existing web interface continues to work unchanged
- No breaking changes to existing functionality

### Rollout Plan
1. **Development**: Implement and test locally
2. **Staging**: Deploy to staging environment for integration testing
3. **Production**: Gradual rollout with feature flags if needed

## Success Criteria

### Functional
- ✅ All read operations work via API
- ✅ Authentication and authorization enforced
- ✅ Proper error handling and validation
- ✅ Business Plugin Middleware can read client data

### Performance
- ✅ Response times under 500ms for typical queries
- ✅ Pagination handles large datasets efficiently
- ✅ Search operations are fast and accurate

### Quality
- ✅ Comprehensive test coverage (>80%)
- ✅ API documentation is complete and accurate
- ✅ No security vulnerabilities introduced

## Risk Assessment

### Low Risk
- Database schema changes: None required
- Backward compatibility: Maintained
- Authentication: Uses existing proven system
- Read-only operations: No data modification risks

### Medium Risk
- API design consistency: Must match existing patterns
- Error handling: Comprehensive coverage needed
- Performance: Large client datasets may need optimization

### Mitigation Strategies
- Follow existing API patterns from invoices.py
- Comprehensive testing before deployment
- Gradual rollout with monitoring

## Timeline Estimate (Simplified)

- **Implementation**: 2-3 days
- **Testing**: 1-2 days
- **Documentation**: 1 day
- **Total**: 4-6 days

## Dependencies

### Technical Dependencies
- FastAPI framework (already in use)
- SQLAlchemy ORM (already in use)
- Existing authentication system

### External Dependencies
- Business Plugin Middleware testing
- Stakeholder approval for API design

## Future Enhancement Path

Once read-only API is stable, future phases can add:
- **Phase 2**: Create operations (POST)
- **Phase 3**: Update operations (PUT)
- **Phase 4**: Delete operations (DELETE)
- **Phase 5**: Bulk operations and advanced filtering

## Next Steps

1. **Approval**: Get stakeholder approval for read-only plan
2. **Kickoff**: Schedule implementation start
3. **Development**: Implement read-only endpoints
4. **Testing**: Regular testing with Business Plugin Middleware
5. **Documentation**: Update API specification

---

*This simplified read-only plan provides immediate value to the Business Plugin Middleware while maintaining safety and simplicity. Full CRUD operations can be added in future phases as needed.*</content>
<parameter name="filePath">/home/chris/InvoicePlanePy/clients-api-plan.md
