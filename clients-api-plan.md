# Clients API Implementation Plan

## Overview
This document outlines the plan to implement a comprehensive JSON API for client management in InvoicePlanePy, enabling the Business Plugin Middleware to programmatically access and manage client/contact information.

## Current State Analysis

### ✅ What Exists
- **Client Model**: Complete SQLAlchemy model with contact fields (phone, email, address, etc.)
- **Web Interface**: Full CRUD operations via HTML templates
- **Database Schema**: Clients table with all necessary fields
- **Authentication**: API key and JWT authentication systems

### ❌ What's Missing
- **JSON API Endpoints**: No `/clients/api` endpoints for programmatic access
- **API Documentation**: Clients API marked as "planned for future release"
- **Contact Separation**: No separate contacts system (contacts are embedded in clients)

## Requirements

### Functional Requirements
1. **List Clients**: Paginated client listing with search and filtering
2. **Get Client Details**: Retrieve complete client information including contact details
3. **Create Clients**: Add new clients via API
4. **Update Clients**: Modify existing client information
5. **Delete Clients**: Soft delete clients (deactivate)
6. **Search & Filter**: Search by name, email, phone, company
7. **Contact Management**: Handle multiple contact methods per client

### Technical Requirements
1. **RESTful Design**: Standard HTTP methods (GET, POST, PUT, DELETE)
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

## API Endpoints Design

### 1. GET /clients/api - List Clients
**Purpose**: Retrieve paginated list of clients with optional filtering and search.

**Query Parameters**:
- `page` (int, default: 1): Page number
- `limit` (int, default: 100, max: 1000): Items per page
- `search` (string, optional): Search in name, email, company, phone
- `is_active` (boolean, optional): Filter by active status
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

### 3. POST /clients/api - Create Client
**Purpose**: Create a new client.

**Request Body**: Client object without `id`, `created_at`, `updated_at`.

**Response**: Created client object with generated fields.

### 4. PUT /clients/{client_id}/api - Update Client
**Purpose**: Update an existing client.

**Request Body**: Partial client object with fields to update.

**Response**: Updated client object.

### 5. DELETE /clients/{client_id}/api - Delete Client
**Purpose**: Soft delete a client (set is_active = false).

**Response**: Success confirmation.

## Implementation Steps

### Phase 1: Core API Endpoints (Priority: High)
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

### Phase 2: CRUD Operations (Priority: Medium)
5. **Implement POST /clients/api**
   - Add input validation using Pydantic models
   - Handle client creation with proper error handling
   - Return created client data

6. **Implement PUT /clients/{client_id}/api**
   - Add partial update logic
   - Validate input and permissions
   - Return updated client data

7. **Implement DELETE /clients/{client_id}/api**
   - Add soft delete functionality
   - Ensure proper permission checks

### Phase 3: Advanced Features (Priority: Low)
8. **Add Advanced Filtering**
   - Company-based filtering
   - Date range filtering
   - Geographic filtering

9. **Add Bulk Operations**
   - Bulk create/update endpoints
   - Bulk status changes

10. **Add Export Features**
    - CSV/Excel export endpoints
    - Custom field support

## Testing Strategy

### Unit Tests
- Test each endpoint with valid/invalid inputs
- Test authentication and authorization
- Test pagination and filtering logic
- Test error handling scenarios

### Integration Tests
- Test with Business Plugin Middleware
- Test with various client data scenarios
- Test concurrent access scenarios

### API Testing Examples
```bash
# List clients
curl -X GET "http://localhost:8000/clients/api?page=1&limit=10&search=john" \
  -H "Authorization: Bearer sk_your_api_key"

# Get specific client
curl -X GET "http://localhost:8000/clients/123/api" \
  -H "Authorization: Bearer sk_your_api_key"

# Create client
curl -X POST "http://localhost:8000/clients/api" \
  -H "Authorization: Bearer sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "company": "Tech Corp",
    "phone": "+1-555-0199"
  }'
```

## Documentation Updates

### API Specification Updates
1. **Update INVOICEPLANEPY_API_SPECIFICATION.md**
   - Replace "planned for future release" note
   - Add complete endpoint documentation
   - Include request/response examples
   - Add error code documentation

2. **Add Usage Examples**
   - Business Plugin Middleware integration examples
   - Client synchronization scenarios
   - Bulk import/export examples

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
- ✅ All CRUD operations work via API
- ✅ Authentication and authorization enforced
- ✅ Proper error handling and validation
- ✅ Business Plugin Middleware can sync clients

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

### Medium Risk
- API design consistency: Must match existing patterns
- Error handling: Comprehensive coverage needed
- Performance: Large client datasets may need optimization

### Mitigation Strategies
- Follow existing API patterns from invoices.py
- Comprehensive testing before deployment
- Gradual rollout with monitoring

## Timeline Estimate

- **Phase 1 (Core API)**: 2-3 days
- **Phase 2 (CRUD Operations)**: 2-3 days
- **Phase 3 (Advanced Features)**: 1-2 days
- **Testing & Documentation**: 2-3 days
- **Total**: 7-11 days

## Dependencies

### Technical Dependencies
- FastAPI framework (already in use)
- SQLAlchemy ORM (already in use)
- Pydantic for validation (already in use)
- Existing authentication system

### External Dependencies
- Business Plugin Middleware testing
- Stakeholder approval for API design

## Next Steps

1. **Approval**: Get stakeholder approval for this plan
2. **Kickoff**: Schedule implementation start
3. **Development**: Begin with Phase 1 implementation
4. **Testing**: Regular testing with Business Plugin Middleware
5. **Documentation**: Keep API specification updated

---

*This plan ensures InvoicePlanePy has a complete, production-ready Clients API that integrates seamlessly with the Business Plugin Middleware while maintaining backward compatibility and following established patterns.*</content>
<parameter name="filePath">/home/chris/InvoicePlanePy/clients-api-plan.md
