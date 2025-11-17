using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NagyprojektBackend.Data;
using NagyprojektBackend.Models;

namespace NagyprojektBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class UsersController : ControllerBase
    {
        private readonly AppDbContext _db;
        public UsersController(AppDbContext db) => _db = db;

        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            var user = _db.Users.Find(id);
            if (user == null) return NotFound();
            return Ok(new { user.Id, user.Username, user.DisplayName, user.Email, user.Role });
        }

        [HttpPut("{id}")]
        public IActionResult Update(int id, [FromBody] UserUpdateDto dto)
        {
            var user = _db.Users.Find(id);
            if (user == null) return NotFound();

            user.DisplayName = dto.DisplayName ?? user.DisplayName;
            user.Email = dto.Email ?? user.Email;
            _db.SaveChanges();
            return Ok(user);
        }
    }

    public record UserUpdateDto(string? DisplayName, string? Email);
}